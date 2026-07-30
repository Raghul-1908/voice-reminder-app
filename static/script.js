document.addEventListener("DOMContentLoaded", () => {

    const startBtn = document.getElementById('start-btn');
    const btnText = document.getElementById('btn-text');
    const listeningIndicator = document.getElementById('listening-indicator');
    const speechResult = document.getElementById('speech-result');
    const aiResult = document.getElementById('ai-result');

    startBtn.onclick = async () => {

        btnText.innerText = "RECORDING...";
        listeningIndicator.classList.remove('hidden');

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const chunks = [];

        mediaRecorder.ondataavailable = e => chunks.push(e.data);

        mediaRecorder.onstop = async () => {

            btnText.innerText = "PROCESSING...";
            listeningIndicator.classList.add('hidden');

            const blob = new Blob(chunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append("audio", blob);

            try {
                // 1️⃣ Whisper transcription
                const transcribeResponse = await fetch("/transcribe", {
                    method: "POST",
                    body: formData
                });

                const transcription = await transcribeResponse.json();
                speechResult.innerText = `"${transcription.text}"`;

                // 2️⃣ Send to BTLM
                const aiResponse = await fetch("/personal-ai", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: transcription.text })
                });

                const aiData = await aiResponse.json();
                aiResult.innerText = aiData.reply || "No response.";

                // 3️⃣ Speak response
                if (aiData.reply) {
                    const msg = new SpeechSynthesisUtterance(aiData.reply);
                    msg.rate = 0.9;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(msg);
                }

            } catch (err) {
                aiResult.innerText = "Error processing audio.";
            }

            stream.getTracks().forEach(track => track.stop());
            btnText.innerText = "START SPEAKING";
        };

        mediaRecorder.start();

        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000); // 5 seconds recording
    };

});
