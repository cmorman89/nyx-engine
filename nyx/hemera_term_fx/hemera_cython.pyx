import numpy as np
cimport numpy as np
from libc.stdio cimport printf

def _c_hemera_print(np.ndarray[np.uint8_t, ndim=2] new_frame, np.ndarray[np.uint8_t, ndim=3] old_subpixel_frame, np.ndarray[str, ndim=1] ansi_fg_map, np.ndarray[str, ndim=1] ansi_bg_map):
    cdef np.ndarray[np.uint8_t, ndim=3] subpixel_frame = _c_calc_subpixel_frame(new_frame)
    cdef np.ndarray[np.uint8_t, ndim=3] delta_frame = _c_calc_delta_frame(subpixel_frame, old_subpixel_frame)
    cdef np.ndarray[np.uint8_t, ndim=2] sum_frame = _c_calc_sum_frame(delta_frame)
    cdef np.ndarray[np.uint16_t, ndim=1] row_sums = _c_calc_row_sums(sum_frame)
    # cdef np.ndarray[np.uint8_t, ndim=2] fg_subframe = _c_split_frame(subpixel_frame[0, :, :])
    cdef str string_buffer = _c_generate_string_buffer(delta_frame[0, :, :], sum_frame, row_sums, ansi_fg_map, ansi_bg_map)
    _c_print_buffer(string_buffer)

cdef np.ndarray[np.uint8_t, ndim=2] _c_split_frame(np.ndarray[np.uint8_t, ndim=3] subpixel_frame):
    cdef np.ndarray[np.uint8_t, ndim=2] fg_subframe = subpixel_frame[0, :, :]
    return fg_subframe

cdef np.ndarray[np.uint8_t, ndim=3] _c_calc_subpixel_frame(np.ndarray[np.uint8_t, ndim=2] frame):
    cdef int h  = frame.shape[0] // 2
    return np.stack([frame[:h:2, :], frame[1:h:2, :]])

cdef np.ndarray[np.uint8_t, ndim=2] _c_generate_blank_frame(int h, int w):
    return np.zeros((2, h, w), dtype=np.uint8)

cdef np.ndarray[np.uint8_t, ndim=3] _c_calc_delta_frame(np.ndarray[np.uint8_t, ndim=3] new_subpixel_frame, np.ndarray[np.uint8_t, ndim=3] old_subpixel_frame):
    return np.where(
        np.any(
            new_subpixel_frame != old_subpixel_frame,
            axis=0,
            keepdims=True),
            new_subpixel_frame,
            np.zeros_like(new_subpixel_frame),
    )

cdef np.ndarray[np.uint16_t, ndim=2] _c_calc_sum_frame(np.ndarray[np.uint8_t, ndim=3] delta_frame):
    return np.sum(delta_frame, axis=0)

cdef np.ndarray[np.uint16_t, ndim=1] _c_calc_row_sums(np.ndarray[np.uint16_t, ndim=2] frame):
    cdef int h = frame.shape[0]
    cdef np.ndarray[np.uint16_t, ndim=1] row_sums = np.zeros(h, dtype=np.uint16)

    for y in range(h):
        row_sums[y] = np.sum(frame[y, :])

    return row_sums

cdef str _c_generate_string_buffer(
    np.ndarray[np.uint8_t, ndim=1] delta_frame,
    np.ndarray[np.uint16_t, ndim=2] sum_frame,
    np.ndarray[np.uint16_t, ndim=1] row_sums,
    np.ndarray[str, ndim=1] ansi_fg_map,
    np.ndarray[str, ndim=1] ansi_bg_map
):
    cdef int h = delta_frame.shape[0]
    cdef int w = delta_frame.shape[1]
    cdef np.uint8_t fg_color = 0
    cdef np.uint8_t bg_color = 0
    cdef np.uint16_t sum_color = 0
    cdef np.uint8_t current_fg_ansi_color = 0
    cdef np.uint8_t current_bg_ansi_color = 0
    cdef np.uint16_t last_subpixel_sum = 0
    cdef np.uint16_t empty_sum = 0
    cdef list buffer = []


    for y in range(h):

        # Skip rows with no changes
        if row_sums[y] == empty_sum:
            continue
        for x in range(w):
            sum_color = sum_frame[y, x]
            if sum_color == empty_sum:
                continue
            fg_color = delta_frame[y, x]
            bg_color = sum_color - fg_color

            # Skip cursor movement if it's the same row/column as the last printed pixel
            if last_subpixel_sum == empty_sum:
                buffer.append(f"\033[{y + 1};{x + 1}H")

            # Only write color change sequences when necessary (skip if same as last)
            # Foreground color check/caching
            if fg_color != current_fg_ansi_color:
                buffer.append(ansi_fg_map[fg_color])
                current_fg_ansi_color = fg_color
            # Background color check/caching
            if bg_color != current_bg_ansi_color:
                buffer.append(ansi_bg_map[bg_color])
                current_bg_ansi_color = bg_color

            # Add the printed character
            buffer.append("▀")

        # Cache the last sum
        last_subpixel_sum = sum_color

    # Add the row buffer for the changed row
    buffer.append("\n")
    return "".join(buffer) 

cdef _c_print_buffer(str buffer):
    # printf("%s", buffer.encode("utf-8"))
    pass