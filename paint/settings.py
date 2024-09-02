CURRENT_TOOL = 'Brush'
CURRENT_COLOR = '#000000'
BG_COLOR = '#FFFFFF'
MENU_BG_COLOR = '#4a4a4a'
BRUSH_SIZE = 5
CURRENT_SLIDER_VAL = 5


COLORS = {
    'BLACK': {'Color': '#000000', 'row': 0, 'col': 0, 'hover_color': '#333333'},
    'WHITE': {'Color': '#FFFFFF', 'row': 0, 'col': 1, 'hover_color': '#DDDDDD'},
    'GRAY': {'Color': '#808080', 'row': 0, 'col': 2, 'hover_color': '#A9A9A9'},
    'RED': {'Color': '#FF0000', 'row': 0, 'col': 3, 'hover_color': '#CC0000'},
    'PINK': {'Color': '#FFC0CB', 'row': 1, 'col': 0, 'hover_color': '#FFB6C1'},
    'ORANGE': {'Color': '#FFA500', 'row': 1, 'col': 1, 'hover_color': '#FF8C00'},
    'BROWN': {'Color': '#A52A2A', 'row': 1, 'col': 2, 'hover_color': '#8B0000'},
    'YELLOW': {'Color': '#FFFF00', 'row': 1, 'col': 3, 'hover_color': '#FFD700'},
    'LIME': {'Color': '#00FF00', 'row': 2, 'col': 0, 'hover_color': '#32CD32'},
    'GREEN': {'Color': '#00FF00', 'row': 2, 'col': 1, 'hover_color': '#32CD32'},
    'CYAN': {'Color': '#00FFFF', 'row': 2, 'col': 2, 'hover_color': '#00CED1'},
    'BLUE': {'Color': '#0000FF', 'row': 2, 'col': 3, 'hover_color': '#0000CD'},
    'NAVY': {'Color': '#000080', 'row': 3, 'col': 0, 'hover_color': '#191970'},
    'PURPLE': {'Color': '#800080', 'row': 3, 'col': 1, 'hover_color': '#9932CC'},
    'MAGENTA': {'Color': '#FF00FF', 'row': 3, 'col': 2, 'hover_color': '#FF66FF'},
    'OLIVE': {'Color': '#808000', 'row': 3, 'col': 3, 'hover_color': '#6B8E23'},
}

TOOLS = {
    'Paint Bucket': {'row': 5, 'col': 0, 'columnspan': 1, 'text': 'Bucket'},
    'Line': {'row': 5, 'col': 1, 'columnspan': 1, 'text': 'Line'},
    'Square': {'row': 5, 'col': 2, 'columnspan': 1, 'text': 'Square'},
    'Circle': {'row': 5, 'col': 3, 'columnspan': 1, 'text': 'Circle'},
    'Paint Brush': {'row': 6, 'col': 0, 'columnspan': 4, 'text': 'Brush'}
}

BRUSH_THICKNESS_SLIDER = {
    'SLIDER': {'row': 7, 'col': 0, 'columnspan': 3, 'max': 25, 'min': 1, 'default': CURRENT_SLIDER_VAL, 'button color': CURRENT_COLOR},
    'SLIDER TEXT': {'row': 7, 'col': 3, 'columnspan': 1, 'text': BRUSH_SIZE}
}

EXTRA = {
    'CLEAR': {'text': 'Clear', 'row': 8, 'col': 0, 'columnspan': 4},
    'CUSTOM_COLOR': {'text': 'Custom Color', 'row': 9, 'col': 0, 'columnspan': 4}
}

