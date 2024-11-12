from kivy.properties import BooleanProperty, NumericProperty
from kivy.clock import Clock

__author__ = "noEmbryo"
__version__ = "0.7.0.0"

__all__ = ("ButtonExtraBehavior",)


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class ButtonExtraBehavior(object):
    """ This `mixin <https://en.wikipedia.org/wiki/Mixin>`_ class adds
    right/middle/double/long click/press/scroll events to any widget.

    :Events:
        `on_long_press`
            Fired after the button is held for more than a customizable
            `long_time`.
        `on_right_click`
            Fired when the right button of a mouse is pressed.
        `on_middle_click`
            Fired when the middle (scroll) button of a mouse is pressed
        `on_double_click`
            Fired if a second click (tap) occurs inside a customizable
            `double_time`. This is disabled by default.
        `on_scroll_up`
            Fired when the mouse wheel scrolls up.
        `on_scroll_down`
            Fired when the mouse wheel scrolls down.
    """

    long_time = NumericProperty(.25)
    """ Minimum time that a click/press must be held, to be registered
    as a `long press`.

    :attr:`long_time` is a float and defaults to 0.25.
    """

    double_time = NumericProperty(.2)
    """ Maximum time for a second click/tap to be registered as `double click`.

    :attr:`double_time` is a float and defaults to 0.2.
    """

    double_click_enabled = BooleanProperty(False)
    """ Enables the double click detection. This introduces a delay to the
    `on_touch_down` emission in the case of a single click.

    :attr:`double_click_enabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    scroll_timeout = NumericProperty()
    """ Timeout that is needed if we use :class:`ButtonExtraBehavior` inside a
    :class:`ScrollView` widget. Must be close to the
    :attr:`~ScrollView.scroll_timeout` value.
    Needed only if :attr:`~ButtonExtraBehavior.double_click_enabled` is `True`.

    :attr:`scroll_timeout` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    """

    def __init__(self, **kwargs):
        super(ButtonExtraBehavior, self).__init__(**kwargs)

        for i in ("on_double_click", "on_middle_click", "on_right_click",
                  "on_long_press", "on_scroll_up", "on_scroll_down"):
            self.register_event_type(i)

        self._long_clock = Clock.schedule_once(self.long_pressed,
                                               self.long_time)
        self._long_clock.cancel()
        self._after_long_press = False

        self._double_clock = Clock.schedule_once(self.send_press,
                                                 self.double_time)
        self._double_clock.cancel()
        self._second_click = False

        self._current_touch = None

    def on_scroll_timeout(self, __, timeout):
        self.long_time = self.long_time + timeout * .001
        self._long_clock = Clock.schedule_once(self.long_pressed,
                                               self.long_time)
        self._long_clock.cancel()

        self.double_time = self.double_time + timeout * .001
        self._double_clock = Clock.schedule_once(self.send_press,
                                                 self.double_time)
        self._double_clock.cancel()

    def on_touch_down(self, touch):
        for child in self.children[:]:
            if child.dispatch("on_touch_down", touch):
                return True
        if self.collide_point(*touch.pos):
            self._current_touch = touch
            self._after_long_press = False
            self._second_click = False
            if "button" in touch.profile:
                if touch.button == "right":
                    self.dispatch("on_right_click")
                    return True  # block release if right click is emitted
                elif touch.button == "middle":
                    self.dispatch("on_middle_click")
                    return True  # block release if middle click is emitted
                elif touch.button == "scrollup":
                    self.dispatch("on_scroll_up")
                    return True  # block release if scroll up is emitted
                elif touch.button == "scrolldown":
                    self.dispatch("on_scroll_down")
                    return True  # block release if scroll down is emitted

            self._long_clock()
            if self._double_clock.is_triggered:  # if double click
                self._second_click = True
                self.state = "down"
                self._double_clock.cancel()
                self.dispatch("on_double_click")
                return True  # block release if double click is emitted
            elif self.double_click_enabled:  # start checking for double click
                self._double_clock()
                self.state = "down"
                return True
            else:
                return super(ButtonExtraBehavior, self).on_touch_down(touch)

    def on_touch_up(self, touch, *__):
        for child in self.children[:]:
            if child.dispatch("on_touch_up", touch):
                return True
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                return True  # just block scrollWheel release
            if self._long_clock.is_triggered:
                self._long_clock.cancel()
                if self.double_click_enabled:
                    if self._second_click:
                        self.state = "normal"
                    return True  # block release while waiting for double click
                else:
                    self.state = "normal"
            else:
                if self._second_click:
                    self.state = "normal"
                    return True  # block release if double click is emitted
                if self._after_long_press:
                    self.state = "normal"
                    return True  # block release if long press is emitted
            return super(ButtonExtraBehavior, self).on_touch_up(touch)

    def send_press(self, *__):
        """ Propagates the `touch_down` event
        """
        if self._long_clock.is_triggered:
            self.state = "down"
        else:
            if not self.scroll_timeout:
                super(ButtonExtraBehavior,
                      self).on_touch_down(self._current_touch)
                self._current_touch.ud[self] = True
                self._current_touch.grab_current = self
                super(ButtonExtraBehavior,
                      self).on_touch_up(self._current_touch)
            else:
                try:
                    super(ButtonExtraBehavior, self).trigger_action()
                except AttributeError:  # no ButtonBehavior in MixIn
                    pass
            self.state = "normal"

    def long_pressed(self, *__):
        """ Sends the "on_long_press" event
        """
        self._after_long_press = True
        self.dispatch("on_long_press")
        self._double_clock.cancel()

    def on_long_press(self):
        """ Needed for the "on_long_press" event """

    def on_right_click(self):
        """ Needed for the "on_right_click" event """

    def on_middle_click(self):
        """ Needed for the "on_middle_click" event """

    def on_double_click(self):
        """ Needed for the "on_double_click" event """

    def on_scroll_up(self):
        """ Needed for the "on_scroll_up" event """

    def on_scroll_down(self):
        """ Needed for the "on_scroll_down" event """
