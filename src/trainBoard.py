import json
import logging
import os
from datetime import datetime
from tkinter import *

from trains import TrainApi

logger = logging.getLogger("station_board")

BOARD_FONT = "London Underground"
BOARD_FONT_SIZE = 24
BOARD_FONT_COLOUR = "white"


class ServiceRow:

    def __init__(self, root, font_scale=1):

        root = root

        self.departureTimeText = StringVar(root)
        self.destinationText = StringVar(root)
        self.statusText = StringVar(root)

        self.departureTime = Label(
            root,
            textvariable=self.departureTimeText,
            width=5,
            fg=BOARD_FONT_COLOUR,
            bg="black",
            anchor="w",
            font=(BOARD_FONT, int(BOARD_FONT_SIZE * font_scale)),
        )
        self.departureTime.pack(side=LEFT, padx=(0, 20))

        self.destination = Label(
            root,
            textvariable=self.destinationText,
            fg=BOARD_FONT_COLOUR,
            bg="black",
            anchor="w",
            font=(BOARD_FONT, int(BOARD_FONT_SIZE * font_scale)),
        )
        self.destination.pack(side=LEFT)

        self.status = Label(
            root,
            textvariable=self.statusText,
            fg=BOARD_FONT_COLOUR,
            bg="black",
            anchor="e",
            font=(BOARD_FONT, int(BOARD_FONT_SIZE * font_scale)),
        )
        self.status.pack(side=RIGHT)

    def update(self, departureTime, destination, status):
        self.departureTime.config(width=5)
        self.departureTimeText.set(departureTime)
        self.destinationText.set(destination)
        self.statusText.set(status)

    def setNoService(self):
        self.departureTime.config(width=10)
        self.departureTimeText.set("NO SERVICE")
        self.destinationText.set("")
        self.statusText.set("")


class StationBoard:

    def __init__(
        self,
        station,
        api_token,
        platforms=[1, 2],
        platform_board_width=800,
        platform_board_height=240,
        test=False,
    ):
        self.station = station
        self.test = test

        platform_count = len(platforms)
        station_board_width = platform_board_width
        station_board_height = platform_count * platform_board_height

        root = Tk()
        root.overrideredirect(True)
        root.configure(background="black", cursor="none", menu="")
        root.geometry(f"{station_board_width}x{station_board_height}")
        root.attributes("-type", "dock")

        self.platform_boards = []
        for i, platform in enumerate(platforms):
            if i > 0:
                sep = Frame(root, bg=BOARD_FONT_COLOUR, height=1)
                sep.pack(fill=X)
            self.platform_boards.append(TrainBoard(root, platform))

        root.after(3000, self.switchOverlays)
        root.after(250, self.scrollText)

        self.timeVar = StringVar(root)
        timeText = Label(
            root,
            textvariable=self.timeVar,
            fg=BOARD_FONT_COLOUR,
            bg="black",
            font=(BOARD_FONT, BOARD_FONT_SIZE),
        )
        timeText.pack(fill=X)
        timeText.after(500, self.updateClock)

        self.trainApi = TrainApi(api_token)

        self.root = root
        self.updateBoards()
        self.root.mainloop()

    def updateBoards(self):
        if self.test:
            logger.info("Loading test data")
            with open(
                os.path.dirname(__file__) + "/../data/test_data.json", "r"
            ) as json_file:
                station_data = json.load(json_file)
            logger.info(f"Loaded {len(station_data)} services from test data")
        else:
            logger.info(f"Fetching live data for station: {self.station}")
            try:
                response = self.trainApi.getStationArrivalsDepartures(self.station)
                if "trainServices" not in response:
                    logger.warning(
                        f"'trainServices' key not found in API response. Full response: {json.dumps(response)}"
                    )
                station_data = response.get("trainServices", [])
                logger.info(f"Received {len(station_data)} services from API")
            except Exception as e:
                logger.error(f"Error fetching station data: {e}")
                station_data = []

        for board in self.platform_boards:
            board.setData(
                self.returnServicesForPlatform(station_data, board.platform_number)
            )
        self.root.after(15000, self.updateBoards)

    def switchOverlays(self):
        for board in self.platform_boards:
            board.switchOverlay()
        self.root.after(3000, self.switchOverlays)

    def scrollText(self):
        for board in self.platform_boards:
            board.incrementTextScroll(1)
        self.root.after(250, self.scrollText)

    def updateClock(self):
        self.timeVar.set(datetime.now().strftime("%H:%M:%S"))
        self.root.after(500, self.updateClock)

    def returnServicesForPlatform(self, stationServices, platform):
        return [
            service
            for service in stationServices
            if service.get("platform", "") == str(platform)
        ]


class TrainBoard:

    def __init__(self, root, platform_number):
        self.platform_number = platform_number
        screen = Frame(root, background="black")
        screen.grid_propagate(0)
        screen.pack(fill=BOTH, expand=1)
        screen.grid_columnconfigure(0, weight=1, uniform="col")
        screen.grid_columnconfigure(1, weight=7, uniform="col")
        for row in [0, 1, 2, 4]:
            screen.grid_rowconfigure(row, weight=1, uniform="row")
        screen.grid_rowconfigure(3, weight=0)

        platform_canvas = Canvas(screen, bg="black", highlightthickness=0)
        platform_canvas.grid(row=0, column=0, rowspan=5, sticky="nesw")
        platform_canvas.bind(
            "<Configure>",
            lambda event: draw_platform_number(platform_number, platform_canvas, event),
        )

        self.root = screen
        self.rowA = Frame(screen, bg="black")
        self.rowB = Frame(screen, bg="black")
        self.rowC = Canvas(screen, bg="black", highlightthickness=0)
        self.rowC._num_carriages = 0
        self.rowD = Frame(screen, bg="black")
        self.rowE = Frame(screen, bg="black")

        self.rowA.grid(row=0, column=1, sticky="nesw")
        self.rowB.grid(row=1, column=1, sticky="nesw")
        self.rowC.grid(row=2, column=1, sticky="nesw")
        self.rowC.bind("<Configure>", lambda e: draw_carriages(self.rowC, e))

        self.separator = Canvas(screen, bg="black", height=1, highlightthickness=0)
        self.separator.grid(row=3, column=1, sticky="ew")
        self.separator.bind(
            "<Configure>", lambda e: draw_dotted_line(self.separator, e)
        )

        self.rowE.grid(row=4, column=1, sticky="nesw")
        self.rowD.grid(row=4, column=1, sticky="nesw")

        self.service1st = ServiceRow(self.rowA)
        self.service2nd = ServiceRow(self.rowD, font_scale=0.75)
        self.service3rd = ServiceRow(self.rowE, font_scale=0.75)

        self.rowB1text = StringVar(screen)
        self.rowB2text = StringVar(screen)

        self.overlayRows = [self.rowD, self.rowE]

        self.currentServices = []

        # self.rowB2text = ""
        self.leadingScroll = -7
        self.scrollPosition = self.leadingScroll
        self.trailingSroll = 10

        rowB1 = Label(
            self.rowB,
            textvariable=self.rowB1text,
            fg=BOARD_FONT_COLOUR,
            bg="black",
            anchor="w",
            font=(BOARD_FONT, BOARD_FONT_SIZE),
        )
        rowB1.pack(side=LEFT, padx=(0, 20))

        self.rowB2 = Entry(
            self.rowB,
            textvariable=self.rowB2text,
            fg=BOARD_FONT_COLOUR,
            bg="black",
            bd=0,
            font=(BOARD_FONT, BOARD_FONT_SIZE),
            state="readonly",
            readonlybackground="black",
            relief="flat",
            highlightthickness=0,
        )
        self.rowB2.pack(side=LEFT)

    def switchOverlay(self):
        self.overlayRows.reverse()
        self.overlayRows[0].tkraise()

    def generateCallingPointsString(self, callingPoints):
        callingPointsInfo = [
            f"{callingPoint['locationName']} ({callingPoint['st']})"
            for callingPoint in callingPoints
        ]
        if len(callingPointsInfo) == 1:
            return callingPointsInfo[0]
        else:
            return (
                ", ".join(callingPointsInfo[:-1])
                + " and "
                + callingPointsInfo[-1]
                + "."
            )

    def incrementTextScroll(self, number):
        if self.scrollPosition <= 0:
            self.scrollPosition += number
            return
        elif self.scrollPosition == len(self.rowB2text.get()):
            self.scrollPosition = self.leadingScroll
            self.rowB2.xview_scroll(-len(self.rowB2text.get()) - 1, UNITS)
            return
        else:
            self.scrollPosition += number
            self.rowB2.xview(MOVETO, self.scrollPosition / len(self.rowB2text.get()))

    def hideRows(self):
        self.rowA.grid_remove()
        self.rowB.grid_remove()
        self.rowC.grid_remove()
        self.rowD.grid_remove()
        self.rowE.grid_remove()

    def showRows(self):
        self.rowA.grid()
        self.rowB.grid()
        self.rowC.grid()
        self.rowD.grid()
        self.rowE.grid()

    def extractDataFromService(self, service):
        """
        Extract all relevant data from a service object.

        Returns:
            dict: Service data including departure time, destination, status,
                  carriages, operator, and calling points
        """
        return {
            "departureTime": service["std"],
            "destination": service["destination"][0]["locationName"],
            "status": service["etd"],
            "carriages": service.get("length", 0),
            "operator": service.get("operator", "Unknown"),
            "callingPoints": service.get("subsequentCallingPoints", [{}])[0].get(
                "callingPoint", []
            ),
        }

    def setData(self, services):
        """
        A wrapper around setData2 so that we can hide data and create a callback to setData2
        in the event of a change to service, simulating a momentary blank screen without halting
        the rest of the program.
        """

        # If services is [] (no services) and currentServices is [], it could be that the app
        # has just started up and its late at night (so no further services). We still want
        # want to set data in this scenario to display NO SERVICE.
        if services == [] and self.currentServices == []:
            self.setData2(services)
            return
        elif services[:3] == self.currentServices:
            logger.info(f"No change in services, not updating display")
            logger.info(
                f"Full retrieved service data: {json.dumps(services, default=str)}"
            )
            return
        else:
            self.hideRows()
            self.root.after(500, self.setData2, services)

    def process_service(self, service_index, service_row, services):
        """
        Process and display a single service.

        Args:
            service_index: 0, 1, or 2 (service position)
            service_row: ServiceRow object to update
            services: List of service objects
        """
        try:
            service = services[service_index]
            data = self.extractDataFromService(service)
            logger.info(
                f"Extracted data for service {service_index + 1}: {json.dumps(data)}"
            )
            service_row.update(
                data["departureTime"], data["destination"], data["status"]
            )

            # Special handling for primary service (index 0)
            if service_index == 0:
                self.rowB1text.set("Calling at:")
                self.rowB2text.set(
                    self.generateCallingPointsString(data["callingPoints"])
                )
                self.scrollPosition = self.leadingScroll
                self.rowC._num_carriages = data["carriages"]
                draw_carriages(self.rowC)
        except IndexError:
            logger.info(f"No service {service_index + 1} available")
            service_row.setNoService()
            if service_index == 0:
                self.rowC.delete("all")

    def setData2(self, services):
        self.process_service(0, self.service1st, services)
        self.process_service(1, self.service2nd, services)
        self.process_service(2, self.service3rd, services)

        self.currentServices = services[:3]
        self.showRows()


def draw_platform_number(platform_number, platform_canvas, event=None):
    platform_canvas.delete("all")
    w = event.width
    h = event.height
    # w = platform_canvas.winfo_width()
    # h = platform_canvas.winfo_height()
    margin = 8

    # dotted border around the whole platform area
    platform_canvas.create_rectangle(
        margin, margin, w - margin, h - margin, outline=BOARD_FONT_COLOUR, dash=(1, 3)
    )

    # "Plat" label in the top third
    platform_canvas.create_text(
        w // 2,
        h // 3,
        text="Plat",
        fill=BOARD_FONT_COLOUR,
        font=(BOARD_FONT, BOARD_FONT_SIZE),
    )

    # platform number filling the bottom two thirds
    platform_canvas.create_text(
        w // 2,
        h // 3 + h // 3,
        text=str(platform_number),
        fill=BOARD_FONT_COLOUR,
        font=(BOARD_FONT, BOARD_FONT_SIZE * 2),
    )


def draw_dotted_line(canvas, event):
    canvas.delete("all")
    canvas.create_line(0, 0, event.width, 0, fill=BOARD_FONT_COLOUR, dash=(1, 3))


def draw_carriages(canvas, event=None):
    canvas.delete("all")
    h = event.height if event else canvas.winfo_height()
    if h <= 1:
        return
    margin = h // 4
    carriage_height = h - margin
    carriage_width = carriage_height * 1.25
    triangle_width = carriage_height // 2

    if canvas._num_carriages:
        draw_canvas_triangle(canvas, triangle_width, carriage_height)

    for i in range(canvas._num_carriages):
        x = triangle_width + i * carriage_width
        canvas.create_rectangle(
            x,
            0,
            x + carriage_width,
            carriage_height,
            outline=BOARD_FONT_COLOUR,
            width=1,
            dash=(1, 3),
        )


def draw_canvas_triangle(canvas, width, height):
    """Draw a right-angled triangle on a canvas with a dot-matrix style.
    Right angle at bottom-right, vertical edge on the right, base on the bottom."""
    # filled triangle with stipple dot-matrix pattern
    canvas.create_polygon(
        width,
        0,
        width,
        height,
        0,
        height,
        outline=BOARD_FONT_COLOUR,
        fill=BOARD_FONT_COLOUR,
        stipple="gray25",
        width=1,
        dash=(1, 3),
    )
