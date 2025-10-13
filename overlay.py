# import AppKit
# from PyObjCTools import AppHelper

# class OverlayWindow(AppKit.NSWindow):
#     def canBecomeKeyWindow(self):
#         return True

#     def keyDown_(self, event):
#         characters = event.characters()
#         if characters.lower() == "r":
#             current = self.ignoresMouseEvents()
#             self.setIgnoresMouseEvents_(not current)
#             print(f"[Toggle] Click-through: {'ON' if not current else 'OFF'}")

# # Screen size and initial window setup
# screen = AppKit.NSScreen.mainScreen().frame()
# width, height = 600, 400
# x = (screen.size.width - width) / 2
# y = (screen.size.height - height) / 2

# # Create the resizable, borderless, transparent window
# window = OverlayWindow.alloc().initWithContentRect_styleMask_backing_defer_(
#     AppKit.NSMakeRect(x, y, width, height),
#     AppKit.NSWindowStyleMaskBorderless | AppKit.NSWindowStyleMaskResizable,
#     AppKit.NSBackingStoreBuffered,
#     False
# )

# window.setLevel_(AppKit.NSStatusWindowLevel + 1)
# window.setOpaque_(False)
# window.setBackgroundColor_(AppKit.NSColor.blackColor().colorWithAlphaComponent_(0.7))
# window.setIgnoresMouseEvents_(False)  # Start interactive
# window.setReleasedWhenClosed_(False)
# window.setHasShadow_(False)
# window.setMovableByWindowBackground_(True)
# window.makeKeyAndOrderFront_(None)
# window.makeFirstResponder_(window)  # So it receives key events

# AppHelper.runEventLoop()

import AppKit
from PyObjCTools import AppHelper

class OverlayWindow(AppKit.NSWindow):
    def initWithContentRect_styleMask_backing_defer_(
        self, rect, style, backing, defer
    ):
        # Proper superclass call
        self = AppKit.NSWindow.initWithContentRect_styleMask_backing_defer_(
            self, rect, style, backing, defer
        )
        if self is None:
            return None

        self.opacity = 0.7
        self.setBackgroundColor_(
            AppKit.NSColor.blackColor().colorWithAlphaComponent_(self.opacity)
        )
        return self

    def canBecomeKeyWindow(self):
        return True

    def keyDown_(self, event):
        characters = event.charactersIgnoringModifiers()
        if characters.lower() == "r":
            current = self.ignoresMouseEvents()
            self.setIgnoresMouseEvents_(not current)
            print(f"[Toggle] Click-through: {'ON' if not current else 'OFF'}")

        elif characters.lower() == "d":
            self.opacity = 1.0
            self.updateOpacity()

        elif characters.lower() == "s":
            self.opacity = min(self.opacity + 0.1, 1.0)
            self.updateOpacity()

        elif characters.lower() == "a":
            self.opacity = max(self.opacity - 0.1, 0.0)
            self.updateOpacity()

    def updateOpacity(self):
        self.setBackgroundColor_(
            AppKit.NSColor.blackColor().colorWithAlphaComponent_(self.opacity)
        )
        print(f"[Opacity] Set to {self.opacity:.1f}")

# Main screen
screen = AppKit.NSScreen.mainScreen().frame()
width, height = 600, 400
x = (screen.size.width - width) / 2
y = (screen.size.height - height) / 2
rect = AppKit.NSMakeRect(x, y, width, height)

# Create window
window = OverlayWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    rect,
    AppKit.NSWindowStyleMaskBorderless | AppKit.NSWindowStyleMaskResizable,
    AppKit.NSBackingStoreBuffered,
    False
)

window.setLevel_(AppKit.NSStatusWindowLevel + 1)
window.setOpaque_(False)
window.setIgnoresMouseEvents_(False)
window.setReleasedWhenClosed_(False)
window.setHasShadow_(False)
window.setMovableByWindowBackground_(True)
window.makeKeyAndOrderFront_(None)
window.makeFirstResponder_(window)

AppHelper.runEventLoop()
