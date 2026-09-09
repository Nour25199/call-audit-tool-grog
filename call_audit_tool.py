import streamlit as st
from groq import Groq


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Call Transcript",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎙️ AI Call Transcript")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    groq_api_key = st.text_input(
        "Enter Groq API Key",
        type="password"
    )

    st.info(
        "Free Mode: Groq Whisper Large V3 Turbo"
    )


# --------------------------------------------------
# UPLOAD AUDIO
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Audio",
    type=[
        "wav",
        "mp3",
        "m4a",
        "mp4",
        "mpeg",
        "mpga",
        "ogg",
        "webm",
        "flac"
    ]
)


if uploaded_file:

    # --------------------------------------------------
    # RESET FOR NEW FILE
    # --------------------------------------------------

    if (
        st.session_state.last_uploaded_file
        != uploaded_file.name
    ):

        st.session_state.transcript = ""

        st.session_state.last_uploaded_file = (
            uploaded_file.name
        )


    # --------------------------------------------------
    # FILE INFO
    # --------------------------------------------------

    file_size_mb = (
        uploaded_file.size / (1024 * 1024)
    )

    st.write(
        f"**File:** {uploaded_file.name}"
    )

    st.write(
        f"**Size:** {file_size_mb:.1f} MB"
    )


    if file_size_mb > 25:

        st.error(
            "This file is larger than 25 MB. "
            "The Groq Free tier accepts audio files "
            "up to 25 MB."
        )

    else:

        # --------------------------------------------------
        # TRANSCRIBE
        # --------------------------------------------------

        if st.button(
            "🚀 Generate Transcript"
        ):

            if not groq_api_key:

                st.warning(
                    "Please enter your Groq API Key."
                )

            else:

                try:

                    client = Groq(
                        api_key=groq_api_key
                    )

                    with st.spinner(
                        "Transcribing... ⚡"
                    ):

                        transcription = (
                            client.audio.transcriptions.create(
                                file=(
                                    uploaded_file.name,
                                    uploaded_file.getvalue()
                                ),
                                model="whisper-large-v3-turbo",
                                response_format="text",
                                temperature=0
                            )
                        )

                        st.session_state.transcript = (
                            transcription
                        )


                    st.success(
                        "✅ Transcript Complete!"
                    )


                except Exception as e:

                    error_text = str(e)

                    if "429" in error_text:

                        st.error(
                            "Groq rate limit reached. "
                            "Please try again later."
                        )

                    else:

                        st.error(
                            f"Transcription Error: {error_text}"
                        )


        # --------------------------------------------------
        # DISPLAY TRANSCRIPT
        # --------------------------------------------------

        if st.session_state.transcript:

            st.subheader("📄 Transcript")

            st.text_area(
                "Transcript:",
                st.session_state.transcript,
                height=500
            )


            # --------------------------------------------------
            # DOWNLOAD
            # --------------------------------------------------

            st.download_button(
                "⬇️ Download Transcript",
                st.session_state.transcript,
                file_name="transcript.txt",
                mime="text/plain"
            )
