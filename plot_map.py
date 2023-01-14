# Preset Data Of Imported Map Image
map_x_bound = (-117.84765, -117.83595)
map_y_bound = (33.64890, 33.64301)

# Preset data box size
data_box = (200, 500)
warning_box  = (500, 150)

# Testing coordinate
test_coordinate = (-117.842871, 33.645698)

# Testing data
test_data = [('latitude', '-117.842871'), ('longitude', '33.645698'), ('sat_count', '1'), ('hdop', '10'), ('mdy', 'na'), ('hmsc', 'na'), ('temp', 'na'), ('packet_count', 'na')]


from PIL import Image # Imported to calculate image size
import pygame as pg # For displaying UI


# define Python user-defined exceptions
class CoordinateOutOfRangeException(Exception):
    """Raised when a given coordinate is out of range"""
    pass


def in_range(map_x_bounds: tuple, map_y_bounds: tuple, coordinates: tuple) -> bool:
    sorted_x_bounds = list(map_x_bounds)
    sorted_y_bounds = list(map_y_bounds)
    sorted_x_bounds.sort()
    sorted_y_bounds.sort()
    return sorted_x_bounds[0] <= coordinates[0] <= sorted_x_bounds[1] and sorted_y_bounds[0] <= coordinates[1] <= sorted_y_bounds[1]


def get_position_on_screen(image_x_dimension: int, image_y_dimension: int, map_x_bounds: tuple, map_y_bounds: tuple, coordinates: tuple) -> tuple:
    # Calculate pixel constants
    x_deg_per_pixel = abs(map_x_bounds[0] - map_x_bounds[1]) / image_x_dimension
    y_deg_per_pixel = abs(map_y_bounds[0] - map_y_bounds[1]) / image_y_dimension
    if in_range(map_x_bounds, map_y_bounds, coordinates):
        # Calculate coordinate position on screen
        position_on_screen = (coordinates[0] - map_x_bounds[0], map_y_bounds[0] - coordinates[1])
        position_on_screen = (position_on_screen[0] / x_deg_per_pixel, position_on_screen[1] / y_deg_per_pixel)
        return position_on_screen
    else:
        raise CoordinateOutOfRangeException


def draw_map(display, map_image, coordinates):
    # Fill background
    display.fill(white)
    # Display map image
    display.blit(map_image, (0, 0))
    # Calculate position on screen
    pos_on_screen = get_position_on_screen(X, Y, map_x_bound, map_y_bound, coordinates)
    # Draw circle on location
    pg.draw.circle(display, light_blue, pos_on_screen, 5)


def draw_text(display, text, text_center, font_size, colour):
    # Create font object
    font = pg.font.Font('freesansbold.ttf', font_size)
    # Print on screen
    text = font.render(text, True, colour)
    textRect = text.get_rect()
    textRect.center = text_center
    display.blit(text, textRect)


def draw_data(display, data_box_rt, data_pairs: [tuple]):

    pg.draw.rect(display, light_blue_2, pg.Rect(X - data_box_rt[0], 0, data_box_rt[0], data_box_rt[1]))

    line_interval = 30

    text_pos = (X - (data_box_rt[0] / 2), 30)

    for name, d in data_pairs:
        draw_text(display, name, text_pos, 20, black)
        text_pos = (text_pos[0], text_pos[1] + line_interval)
        draw_text(display, d, text_pos, 20, grey)
        text_pos = (text_pos[0], text_pos[1] + line_interval)


def draw_warnings(display, warning_box_rb, messages: []):
    pg.draw.rect(display, light_blue_2, pg.Rect(X - warning_box_rb[0], Y - warning_box_rb[1], warning_box_rb[0], warning_box_rb[1]))
    line_interval = 20

    text_pos = (X - (warning_box_rb[0] / 2), Y - warning_box_rb[1] + 20)

    for m in messages:
        draw_text(display, m, text_pos, 20, pink)
        text_pos = (text_pos[0], text_pos[1] + line_interval)


im = Image.open('map_uci_park.png')

X, Y = im.size

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (117, 156, 240)
light_blue_2 = (50, 95, 117)
grey = (217, 217, 228)
pink = (232, 89, 103)

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pg.display.set_mode((X, Y))

# set the pg window name
pg.display.set_caption('TrackBox')

# create a surface object, image is drawn on it.
image = pg.image.load('map_uci_park.png')

# infinite loop
while True:

    draw_map(display_surface, image, test_coordinate)
    draw_data(display_surface, data_box, test_data)
    draw_warnings(display_surface, warning_box, ['This is a test warning'])

    # iterate over the list of Event objects
    # that was returned by pg.event.get() method.
    for event in pg.event.get():

        # if event object type is QUIT
        # then quitting the pg
        # and program both.
        if event.type == pg.QUIT:
            # deactivates the pg library
            pg.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
        pg.display.update()