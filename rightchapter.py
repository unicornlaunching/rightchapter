import streamlit as st
from bokeh.models.widgets import Button, Div
from bokeh.layouts import column
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# Create the Speak button and timer display
stt_button = Button(label="Speak", width=100)
timer_display = Div(text="Timer: 120")

# JavaScript code for the button click event
stt_button.js_on_event("button_click", CustomJS(args=dict(timer_display=timer_display), code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    var timeLeft = 120;
    var finalTranscript = '';
    var timerInterval = setInterval(function() {
        timeLeft--;
        timer_display.text = 'Timer: ' + timeLeft;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            recognition.stop();
        }
    }, 1000);
    
    recognition.onresult = function (e) {
        var interimTranscript = '';
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                finalTranscript += e.results[i][0].transcript;
            } else {
                interimTranscript += e.results[i][0].transcript;
            }
        }
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: finalTranscript + interimTranscript}));
    }

    recognition.start();

    recognition.onend = function() {
        clearInterval(timerInterval);
    }
    """))

# Layout for the button and timer display
layout = column(stt_button, timer_display)

# Event handling in Streamlit
result = streamlit_bokeh_events(
    layout,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=200,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
