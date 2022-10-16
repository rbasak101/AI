# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
# Inspired by work done by Jongdeog Lee (jlee700@illinois.edu)

"""
This file contains geometry functions necessary for solving problems in MP3
"""

import math
import numpy as np
from alien import Alien
from typing import List, Tuple

def does_alien_touch_wall(alien, walls,granularity):
    """Determine whether the alien touches a wall

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            walls (list): List of endpoints of line segments that comprise the walls in the maze in the format [(startx, starty, endx, endx), ...]
            granularity (int): The granularity of the map

        Return:
            True if touched, False if not
    """
    # print("ALIEN: ", alien.get_centroid())
    # print("GRANULARITY: ", granularity, granularity / math.sqrt(2))
    # print("WALLS: ", walls)
    if alien.is_circle():
        center = alien.get_centroid()
        radius = alien.get_width()
        for startx, starty, endx, endy in walls:
            if point_segment_distance(center, ((startx, starty),(endx, endy))) <=  granularity / math.sqrt(2) + radius:
                return True
    else:
        head, tail = alien.get_head_and_tail()
        if head[0] == tail[0]: # vertical alien
            smallest = min(head[1], tail[1])
            largest = max(head[1], tail[1])
            alien_segment = [[head[0], smallest], [head[0], largest]]
            for startx, starty, endx, endy in walls:
                if do_segments_intersect([[startx, starty], [endx, endy]], alien_segment):
                    return True
                if segment_distance([[startx, starty], [endx, endy]], alien_segment) <= granularity / math.sqrt(2) + alien.get_width():
                        return True
                # if starty == endy: 
                #     # print("Horizontal Wall")
                #     if segment_distance([[startx, starty], [endx, endy]], alien_segment) <= granularity / math.sqrt(2) + alien.get_width():
                #         return True
                # else:
                #     # print("Vertical Wall??")
                #     if segment_distance([[startx, starty], [endx, endy]], alien_segment) <= granularity / math.sqrt(2) + alien.get_width():
                #         return True
        
        else: # horizontal alien
            smallest = min(head[0], tail[0])
            largest = max(head[0], tail[0])
            alien_segment = [[smallest, head[1]], [largest, head[1]]]
            for startx, starty, endx, endy in walls:
                if do_segments_intersect([[startx, starty], [endx, endy]], alien_segment):
                    return True
                if segment_distance([[startx, starty], [endx, endy]], alien_segment) <= granularity / math.sqrt(2) + alien.get_width():
                    return True
                # if starty == endy: # horizontal wall
                #     if segment_distance([[startx, starty], [endx, endy]], alien_segment) <= granularity / math.sqrt(2) + alien.get_width():
                #         return True
                # else: 
                #     if segment_distance([[startx, starty], [endx, endy]], alien_segment) <= granularity / math.sqrt(2) + alien.get_width():
                #         return True

    return False

def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """
    """
    ball or sausage
    ball --> center + radius >= goal --> True else False
    sausage --> center +/- length or center + width interesect with goal point --> True else False
    """
    # print("Alien: ", alien.get_centroid())
    # print("Alien shape: ", alien.get_shape())
    # print("Goals: ", goals)

    center = alien.get_centroid()
    if alien.is_circle(): 
        radius = alien.get_width()
        for (x, y, r) in goals:
            distance = math.sqrt((x - center[0]) * (x - center[0]) + (y - center[1]) * (y - center[1]))
            if distance <= r + radius:
                return True
    else:
        head, tail = alien.get_head_and_tail()
        if head[0] == tail[0]: # vertical
            smallest = min(head[1], tail[1])
            largest = max(head[1], tail[1])
            alien_segment = [[head[0], smallest], [head[0], largest]]
            for (x, y, r) in goals:
                if point_segment_distance((x, y), alien_segment) <= r + alien.get_width():
                    return True

        elif head[1] == tail[1]: # horizontal rod
            smallest = min(head[0], tail[0])
            largest = max(head[0], tail[0])
            alien_segment = [[smallest, head[1]], [largest, head[1]]]
            for (x, y, r) in goals:
                if point_segment_distance((x, y), alien_segment) <= r + alien.get_width():
                    return True

    return False

def is_alien_within_window(alien, window,granularity):
    """Determine whether the alien stays within the window
        
        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """
    # print("is_alien_within_window")
    # print(alien.get_centroid())
    # print("window: ", window)
    # print("granularity: ", granularity)
    top_bound = [(0, 0), [window[0], 0]]
    bot_bound = [(0, window[1]), window]
    left_bound = [(0, 0), [0, window[1]]]
    right_bound = [(window[0], 0), window]
    bounds = [("top", top_bound), ("bottom", bot_bound), ("left", left_bound), ("right", right_bound)]
    center = alien.get_centroid()
    if alien.is_circle():
        radius = alien.get_width()
        # print("Ball: ", center, radius)
        for direction, bound in bounds:
            # print("BOUND: ", bound)
            # print("Point to seg distance: ", point_segment_distance(center, bound), point_segment_distance(center, bound) <= granularity / math.sqrt(2) + radius)
            # print(center, bound)
            # print(center[0] <= bound[0][0])
            if point_segment_distance(center, bound) <= granularity / math.sqrt(2) + radius and \
                (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                    return False
    else:
        head, tail = alien.get_head_and_tail()
        if head[0] == tail[0]: # vertical alien
            smallest = min(head[1], tail[1])
            largest = max(head[1], tail[1])
            alien_segment = [[head[0], smallest], [head[0], largest]]
            for direction, bound in bounds:
                if segment_distance(bound, alien_segment) <= granularity / math.sqrt(2) + alien.get_width() and \
                    (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                        print("RETURNING FALSE")
                        return False
                # if direction == "top" or direction == "bottom":
                #     if segment_distance(bound, alien_segment) <= granularity / math.sqrt(2) + alien.get_width() and \
                #         (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                #             print("RETURNING FALSE")
                #             return False
                # else:
                #      if segment_distance(bound, alien_segment) <= granularity / math.sqrt(2) + alien.get_width() and \
                #         (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                #             print("RETURNING FALSE")
                #             return False

        else: # horizontal alien
            smallest = min(head[0], tail[0])
            largest = max(head[0], tail[0])
            alien_segment = [[smallest, head[1]], [largest, head[1]]]
            for direction, bound in bounds:
                if segment_distance(bound, alien_segment) <= granularity / math.sqrt(2) + alien.get_width() and \
                    (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                        return False
                # if direction == "left" or direction == "right":
                #     if segment_distance(bound, alien_segment) <= granularity / math.sqrt(2) + alien.get_width() and \
                #         (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                #             print("RETURNING FALSE")
                #             return False
                # else:
                #     if segment_distance(bound, alien_segment) <= granularity / math.sqrt(2) + alien.get_width() and \
                #         (center[0] <= bound[0][0] or center[0] >= bound[1][0] or center[1] <= bound[0][1] or center[1] >= bound[1][1]):
                #             print("RETURNING FALSE")
                #             return False

    # print(" ")
    return True

def point_segment_distance(point, segment): # helper
    """Compute the distance from the point to the line segment.
    Hint: Lecture note "geometry cheat sheet"

        Args:
            point: A tuple (x, y) of the coordinates of the point.
            segment: A tuple ((x1, y1), (x2, y2)) of coordinates indicating the endpoints of the segment.

        Return:
            Euclidean distance from the point to the line segment.
    """
    """
    3 cases: either return first end, return other end, or some point in between the ends to calculate distance
    """
    if segment[0][0] == segment[1][0] and segment[0][1] == segment[1][1]:
        print("segment is a point!")
        return math.sqrt((point[0] - segment[0][0]) * (point[0] - segment[0][0]) + (point[1] - segment[1][0]) * (point[1] - segment[1][0]))
    # print("Segment: ", segment, "Point: ", point)
    # line segment vector AZ
    vector_line = [None, None]
    vector_line[0] = segment[1][0] - segment[0][0]
    vector_line[1] = segment[1][1] - segment[0][1]

    # let P denote point  #right end vector
    ZP = [None, None]
    ZP[0] = point[0] - segment[1][0]
    ZP[1] = point[1] - segment[1][1]

    #left end vector
    AP = [None, None]
    AP[0] = point[0] - segment[0][0]
    AP[1] = point[1] - segment[0][1]

    AZtoZP = vector_line[0] * ZP[0] + vector_line[1] *  ZP[1] # right
    AZtoAP = vector_line[0] * AP[0] + vector_line[1] *  AP[1] # left

    # print("Vectors: ", vector_line, AP, ZP, AZtoZP, AZtoAP)
    x, y = 0, 0
    if AZtoZP > 0:
        x = point[0] - segment[1][0]
        y = point[1] - segment[1][1]
    elif AZtoAP < 0:
        x = point[0] - segment[0][0]
        y = point[1] - segment[0][1]
    else:  
        """
        Directly perpendicular
        |PQ| = |a|sin(alpha)
        |a||b|sin(alpha) = a X b
        |PQ| = |a|sin(alpha) = (a X b)/ |b|
        """
        cross_product = AP[0] * vector_line[1] - AP[1] * vector_line[0]
        magnitude_b = math.sqrt((segment[1][0] - segment[0][0]) * (segment[1][0] - segment[0][0]) + (segment[1][1] - segment[0][1]) * (segment[1][1] - segment[0][1]))
        return abs(cross_product / magnitude_b)

    return math.sqrt(x * x + y * y)


def do_segments_intersect(segment1, segment2):
    """Determine whether segment1 intersects segment2.  
    We recommend implementing the above first, and drawing down and considering some examples.
    Lecture note "geometry cheat sheet" may also be handy.

        Args:
            segment1: A tuple of coordinates indicating the endpoints of segment1.
            segment2: A tuple of coordinates indicating the endpoints of segment2.

        Return:
            True if line segments intersect, False if not.
    """
    """
    https://algorithmtutor.com/Computational-Geometry/Check-if-two-line-segment-intersect/
    """
    p1, p2, p3, p4 = segment1[0], segment1[1], segment2[0], segment2[1]

    def subtract(A, B):
        return [A[0] - B[0], A[1] - B[1]]

    def on_seg(p1, p2, p):
        return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])

    p1_p3 = subtract(p1, p3)
    p4_p3 = subtract(p4, p3)
    d1 = (p1_p3[0] * p4_p3[1]) - (p1_p3[1] * p4_p3[0])

    p2_p3 = subtract(p2, p3)
    d2 = (p2_p3[0] * p4_p3[1]) - (p2_p3[1] * p4_p3[0])

    p3_p1 = subtract(p3, p1)
    p2_p1 = subtract(p2, p1)
    d3 = (p3_p1[0] * p2_p1[1]) - (p3_p1[1] * p2_p1[0])

    p4_p1 = subtract(p4, p1)
    d4 = (p4_p1[0] * p2_p1[1]) - (p4_p1[1] * p2_p1[0])

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    if (d1 == 0 and on_seg(p3, p4, p1)) or (d2 == 0 and on_seg(p3, p4, p2)) or (d3 == 0 and on_seg(p1, p2, p3)) or \
        (d4 == 0 and on_seg(p1, p2, p4)):
        return True
    return False


def segment_distance(segment1, segment2):
    """
    Compute the distance from segment1 to segment2.  You will need `do_segments_intersect`.
    Hint: Distance of two line segments is the distance between the closest pair of points on both.

        Args:
            segment1: A tuple of coordinates indicating the endpoints of segment1.
            segment2: A tuple of coordinates indicating the endpoints of segment2.

        Return:
            Euclidean distance between the two line segments.
    """
    def euclidean(coord1, coord2):
        x1, y1 = coord1[0], coord1[1]
        x2, y2 = coord2[0], coord2[1]
        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    p1, p2, p3, p4 = segment1[0], segment1[1], segment2[0], segment2[1]
    if do_segments_intersect(segment1, segment2):
        return 0
    
    # try all 4 point to segment combinations and take the min
    p1_seg2 = point_segment_distance(p1, segment2)
    p2_seg2 = point_segment_distance(p2, segment2)
    p3_seg1 = point_segment_distance(p3, segment1)
    p4_seg1 = point_segment_distance(p4, segment1)
    return min(p1_seg2, p2_seg2, p3_seg1, p4_seg1)

if __name__ == '__main__':

    from geometry_test_data import walls, goals, window, alien_positions, alien_ball_truths, alien_horz_truths, \
        alien_vert_truths, point_segment_distance_result, segment_distance_result, is_intersect_result

    # Here we first test your basic geometry implementation
    def test_point_segment_distance(points, segments, results):
        num_points = len(points)
        num_segments = len(segments)
        for i in range(num_points):
            p = points[i]
            for j in range(num_segments):
                seg = ((segments[j][0], segments[j][1]), (segments[j][2], segments[j][3]))
                cur_dist = point_segment_distance(p, seg)
                assert abs(cur_dist - results[i][j]) <= 10 ** -3, \
                    f'Expected distance between {points[i]} and segment {segments[j]} is {results[i][j]}, ' \
                    f'but get {cur_dist}'


    def test_do_segments_intersect(center: List[Tuple[int]], segments: List[Tuple[int]],
                                   result: List[List[List[bool]]]):
        for i in range(len(center)):
            for j, s in enumerate([(40, 0), (0, 40), (100, 0), (0, 100), (0, 120), (120, 0)]):
                for k in range(len(segments)):
                    cx, cy = center[i]
                    st = (cx + s[0], cy + s[1])
                    ed = (cx - s[0], cy - s[1])
                    a = (st, ed)
                    b = ((segments[k][0], segments[k][1]), (segments[k][2], segments[k][3]))
                    if do_segments_intersect(a, b) != result[i][j][k]:
                        if result[i][j][k]:
                            assert False, f'Intersection Expected between {a} and {b}.'
                        if not result[i][j][k]:
                            assert False, f'Intersection not expected between {a} and {b}.'


    def test_segment_distance(center: List[Tuple[int]], segments: List[Tuple[int]], result: List[List[float]]):
        for i in range(len(center)):
            for j, s in enumerate([(40, 0), (0, 40), (100, 0), (0, 100), (0, 120), (120, 0)]):
                for k in range(len(segments)):
                    cx, cy = center[i]
                    st = (cx + s[0], cy + s[1])
                    ed = (cx - s[0], cy - s[1])
                    a = (st, ed)
                    b = ((segments[k][0], segments[k][1]), (segments[k][2], segments[k][3]))
                    distance = segment_distance(a, b)
                    assert abs(result[i][j][k] - distance) <= 10 ** -3, f'The distance between segment {a} and ' \
                                                                  f'{b} is expected to be {result[i]}, but your' \
                                                                  f'result is {distance}'

    def test_helper(alien: Alien, position, truths):
        alien.set_alien_pos(position)
        config = alien.get_config()

        touch_wall_result = does_alien_touch_wall(alien, walls, 0)
        touch_goal_result = does_alien_touch_goal(alien, goals)
        in_window_result = is_alien_within_window(alien, window, 0)

        # assert touch_wall_result == truths[
        #     0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {touch_wall_result}, ' \
        #         f'expected: {truths[0]}'
        # assert touch_goal_result == truths[
        #     1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {touch_goal_result}, ' \
        #         f'expected: {truths[1]}'
        assert in_window_result == truths[
            2], f'is_alien_within_window(alien, window) with alien config {config} returns {in_window_result}, ' \
                f'expected: {truths[2]}'


    # Initialize Aliens and perform simple sanity check.
    alien_ball = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Ball', window)
    test_helper(alien_ball, alien_ball.get_centroid(), (False, False, True))

    alien_horz = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Horizontal', window)
    test_helper(alien_horz, alien_horz.get_centroid(), (False, False, True))

    alien_vert = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Vertical', window)
    test_helper(alien_vert, alien_vert.get_centroid(), (True, False, True))

    edge_horz_alien = Alien((50, 100), [100, 0, 100], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Horizontal',
                            window)
    edge_vert_alien = Alien((200, 70), [120, 0, 120], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Vertical',
                            window)

    centers = alien_positions
    segments = walls
    test_point_segment_distance(centers, segments, point_segment_distance_result)
    test_do_segments_intersect(centers, segments, is_intersect_result)
    test_segment_distance(centers, segments, segment_distance_result)

    for i in range(len(alien_positions)):
        test_helper(alien_ball, alien_positions[i], alien_ball_truths[i])
        test_helper(alien_horz, alien_positions[i], alien_horz_truths[i])
        test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    # Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110, 55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))

    print("Geometry tests passed\n")