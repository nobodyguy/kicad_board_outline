import pcbnew
from pcbnew import wxPoint
import os


def add_line(start, end, layer=pcbnew.Edge_Cuts):
    board = pcbnew.GetBoard()
    segment = pcbnew.PCB_SHAPE(board)
    segment.SetShape(pcbnew.SHAPE_T_SEGMENT)
    segment.SetStart(pcbnew.VECTOR2I(start))
    segment.SetEnd(pcbnew.VECTOR2I(end))
    segment.SetLayer(layer)
    segment.SetWidth(int(0.1 * pcbnew.PCB_IU_PER_MM))
    board.Add(segment)


def add_line_arc(start, center, angle=90, layer=pcbnew.Edge_Cuts):
    board = pcbnew.GetBoard()
    arc = pcbnew.PCB_SHAPE(board)
    arc.SetShape(pcbnew.SHAPE_T_ARC)
    arc.SetStart(pcbnew.VECTOR2I(start))
    arc.SetCenter(pcbnew.VECTOR2I(center))
    arc.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    arc.SetLayer(layer)
    arc.SetWidth(int(0.1 * pcbnew.PCB_IU_PER_MM))
    board.Add(arc)


class BoardOutlinePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Board Outline Generator"
        self.category = "Modify PCB"
        self.description = "Generates outline around your board"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), 'icon.png')

    def Run(self):
        margin_left = 0 * pcbnew.PCB_IU_PER_MM
        margin_right = 0 * pcbnew.PCB_IU_PER_MM
        margin_top = 0 * pcbnew.PCB_IU_PER_MM
        margin_bottom = 0 * pcbnew.PCB_IU_PER_MM

        radius = 2 * pcbnew.PCB_IU_PER_MM
        board = pcbnew.GetBoard()
        board_bb = board.GetBoundingBox()
        board_bb_center = board_bb.GetCenter()
        left_bottom_corner = wxPoint(
            board_bb_center.x - (board_bb.GetWidth() / 2) + margin_left, board_bb_center.y + (board_bb.GetHeight() / 2) + margin_bottom)
        left_top_corner = wxPoint(
            board_bb_center.x - (board_bb.GetWidth() / 2) + margin_left, board_bb_center.y - (board_bb.GetHeight() / 2) + margin_top)
        right_bottom_corner = wxPoint(
            board_bb_center.x + (board_bb.GetWidth() / 2) + margin_right, board_bb_center.y + (board_bb.GetHeight() / 2) + margin_bottom)
        right_top_corner = wxPoint(
            board_bb_center.x + (board_bb.GetWidth() / 2) + margin_right, board_bb_center.y - (board_bb.GetHeight() / 2) + margin_top)

        add_line(wxPoint(left_bottom_corner.x, left_bottom_corner.y - radius),
                 wxPoint(left_top_corner.x, left_top_corner.y + radius))
        add_line(wxPoint(left_top_corner.x + radius, left_top_corner.y),
                 wxPoint(right_top_corner.x - radius, left_top_corner.y))
        add_line(wxPoint(right_bottom_corner.x, right_bottom_corner.y - radius),
                 wxPoint(right_top_corner.x, right_top_corner.y + radius))
        add_line(wxPoint(left_bottom_corner.x + radius, left_bottom_corner.y),
                 wxPoint(right_bottom_corner.x - radius, right_bottom_corner.y))

        add_line_arc(wxPoint(left_bottom_corner.x + radius, left_bottom_corner.y),
                     wxPoint(left_bottom_corner.x + radius, left_bottom_corner.y - radius))
        add_line_arc(wxPoint(left_top_corner.x, left_top_corner.y + radius),
                     wxPoint(left_top_corner.x + radius, left_top_corner.y + radius))
        add_line_arc(wxPoint(right_top_corner.x - radius, right_top_corner.y),
                     wxPoint(right_top_corner.x - radius, right_top_corner.y + radius))
        add_line_arc(wxPoint(right_bottom_corner.x, right_bottom_corner.y - radius),
                     wxPoint(right_bottom_corner.x - radius, right_bottom_corner.y - radius))

        pcbnew.Refresh()
