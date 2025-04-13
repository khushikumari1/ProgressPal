from typing import List, Tuple

def merge_intervals(intervals):
    """
    Merge overlapping or adjacent intervals.
    """
    if not intervals:
        return []
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # If the current interval overlaps or is adjacent to the last merged interval, merge them
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
    
    return merged


def calculate_total_watched(intervals: List[Tuple[float, float]]) -> float:
    """
    Sum total watched seconds from merged intervals.
    """
    merged = merge_intervals(intervals)
    return sum(end - start for start, end in merged)


def calculate_percentage(intervals: List[Tuple[float, float]], video_duration: float) -> float:
    """
    Calculate percentage watched from video.
    """
    if video_duration <= 0:
        return 0.0
    total = calculate_total_watched(intervals)
    return round((total / video_duration) * 100, 2)
