# Chapter 10: Creating Components and Extending Functionality
# Recipe 6: StyledTextCtrl Custom Highlighting
#
import wx
import wx.stc

class BaseLexer(object):
    """Defines simple interface for custom lexer objects"""
    def __init__(self):
        super(BaseLexer, self).__init__()

    def StyleText(self, event):
        raise NotImplementedError

class VowelLexer(BaseLexer):
    """Simple lexer to highlight vowels"""
    # Define some style IDs
    STC_STYLE_VOWEL_DEFAULT, \
    STC_STYLE_VOWEL_KW = range(2)
    def __init__(self):
        super(VowelLexer, self).__init__()
        
        # Attributes
        self.vowels = [ord(char) for char in "aeiouAEIOU"]

    def StyleText(self, event):
        """Handle the EVT_STC_STYLENEEDED event"""
        stc = event.GetEventObject()
        # Last correctly styled character
        last_styled_pos = stc.GetEndStyled()
        # Get styling range for this call
        line = stc.LineFromPosition(last_styled_pos)
        start_pos = stc.PositionFromLine(line)
        end_pos = event.GetPosition()
        # Walk the line and find all the vowels to style
        # Note: little inefficient doing one char at a time
        #       but just to illustrate the process.
        while start_pos < end_pos:
            stc.StartStyling(start_pos, 0x1f)
            char = stc.GetCharAt(start_pos)
            if char in self.vowels:
                # Set Vowel Keyword style
                style = VowelLexer.STC_STYLE_VOWEL_KW
            else:
                # Set Default style
                style = VowelLexer.STC_STYLE_VOWEL_DEFAULT
            # Set the styling byte information for 1 char from
            # current styling position (start_pos) with the
            # given style.
            stc.SetStyling(1, style)
            start_pos += 1

class CustomSTC(wx.stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        super(CustomSTC, self).__init__(*args, **kwargs)

        # Attributes
        self.custlex = None

        # Event Handlers
        self.Bind(wx.stc.EVT_STC_STYLENEEDED, self.OnStyle)

    def OnStyle(self, event):
        # Delegate to custom lexer object if one exists
        if self.custlex:
            self.custlex.StyleText(event)
        else:
            event.Skip()

    def SetLexer(self, lexerid, lexer=None):
        """Overrides StyledTextCtrl.SetLexer
        Adds optional param to pass in custom container
        lexer object.
        """
        self.custlex = lexer
        super(CustomSTC, self).SetLexer(lexerid)

#---- End Recipe Code ----#

class StyledTextApp(wx.App):
    def OnInit(self):
        self.frame = StcFrame(None, title="Custom Lexer")
        self.frame.Show()
        return True

class StcFrame(wx.Frame):
    """Main application window"""
    def __init__(self, parent, *args, **kwargs):
        super(StcFrame, self).__init__(parent,
                                       *args,
                                       **kwargs)

        # Attributes
        self.stc = CustomSTC(self)

        # Setup STC for vowel highlighting
        style = VowelLexer.STC_STYLE_VOWEL_DEFAULT
        self.stc.StyleSetSpec(style, "fore:#000000")
        style = VowelLexer.STC_STYLE_VOWEL_KW
        self.stc.StyleSetSpec(style, "fore:#FF0000,bold")
        self.stc.SetLexer(wx.stc.STC_LEX_CONTAINER,
                          VowelLexer())

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.stc, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((300, 300))

if __name__ == '__main__':
    app = StyledTextApp(False)
    app.MainLoop()
