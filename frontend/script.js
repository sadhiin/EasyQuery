document.addEventListener('DOMContentLoaded', () => {
    const dbUrlInput = document.getElementById('dbUrl');
    const connectDbButton = document.getElementById('connectDb');
    const connectionStatus = document.getElementById('connectionStatus');
    const naturalLanguageQuery = document.getElementById('naturalLanguageQuery');
    const executeQueryButton = document.getElementById('executeQuery');
    const startSpeechButton = document.getElementById('startSpeech');
    const stopSpeechButton = document.getElementById('stopSpeech');
    const queryResults = document.getElementById('queryResults');
    const dbSchemaDisplay = document.getElementById('dbSchema');

    // Speech recognition variables
    let mediaRecorder;
    let audioChunks = [];
    let recognition;

    // Base URL for backend API
    const API_BASE_URL = '/api/v1';

    // --- Database Connection ---
    connectDbButton.addEventListener('click', async () => {
        const dbUrl = dbUrlInput.value;
        if (!dbUrl) {
            connectionStatus.textContent = 'Please enter a database URL.';
            connectionStatus.style.color = 'red';
            return;
        }

        connectionStatus.textContent = 'Connecting...';
        connectionStatus.style.color = 'orange';

        try {
            const response = await fetch(`${API_BASE_URL}/connection/connect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ db_url: dbUrl })
            });
            const data = await response.json();

            if (response.ok) {
                connectionStatus.textContent = `Connected to ${data.db_url}`;
                connectionStatus.style.color = 'green';
                fetchSchema(); // Fetch schema on successful connection
            } else {
                connectionStatus.textContent = `Connection failed: ${data.detail || data.message}`;
                connectionStatus.style.color = 'red';
            }
        } catch (error) {
            console.error('Error connecting to database:', error);
            connectionStatus.textContent = `Connection error: ${error.message}`;
            connectionStatus.style.color = 'red';
        }
    });

    // --- Fetch Database Schema ---
    async function fetchSchema() {
        try {
            const response = await fetch(`${API_BASE_URL}/query/schema`);
            const data = await response.json();

            if (response.ok) {
                dbSchemaDisplay.textContent = JSON.stringify(data.schema, null, 2);
            } else {
                dbSchemaDisplay.textContent = `Failed to fetch schema: ${data.detail || data.message}`;
                dbSchemaDisplay.style.color = 'red';
            }
        } catch (error) {
            console.error('Error fetching schema:', error);
            dbSchemaDisplay.textContent = `Error fetching schema: ${error.message}`;
            dbSchemaDisplay.style.color = 'red';
        }
    }

    // --- Execute Text Query ---
    executeQueryButton.addEventListener('click', async () => {
        const queryText = naturalLanguageQuery.value;
        if (!queryText) {
            queryResults.textContent = 'Please enter a query.';
            queryResults.style.color = 'red';
            return;
        }

        queryResults.textContent = 'Executing query...';
        queryResults.style.color = 'orange';

        try {
            const response = await fetch(`${API_BASE_URL}/query/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query_text: queryText })
            });
            const data = await response.json();

            if (response.ok) {
                queryResults.textContent = JSON.stringify(data.results, null, 2);
                queryResults.style.color = 'black';
            } else {
                queryResults.textContent = `Query failed: ${data.detail || data.message}`;
                queryResults.style.color = 'red';
            }
        } catch (error) {
            console.error('Error executing query:', error);
            queryResults.textContent = `Query error: ${error.message}`;
            queryResults.style.color = 'red';
        }
    });

    // --- Speech Recognition ---
    startSpeechButton.addEventListener('click', async () => {
        startSpeechButton.disabled = true;
        stopSpeechButton.disabled = false;
        queryResults.textContent = 'Listening...';
        queryResults.style.color = 'blue';

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await sendAudioToBackend(audioBlob);
                startSpeechButton.disabled = false;
                stopSpeechButton.disabled = true;
            };

            mediaRecorder.start();
        } catch (error) {
            console.error('Error accessing microphone:', error);
            queryResults.textContent = `Microphone access error: ${error.message}`;
            queryResults.style.color = 'red';
            startSpeechButton.disabled = false;
            stopSpeechButton.disabled = true;
        }
    });

    stopSpeechButton.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            queryResults.textContent = 'Processing speech...';
            queryResults.style.color = 'orange';
        }
    });

    async function sendAudioToBackend(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('audio_file', audioBlob, 'audio.wav');

            const response = await fetch(`${API_BASE_URL}/query/speech-query`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                queryResults.textContent = `Speech Query: "${data.text_query}"\nSQL: "${data.sql_query}"\nResults: ${JSON.stringify(data.results, null, 2)}`;
                queryResults.style.color = 'black';
            } else {
                queryResults.textContent = `Speech query failed: ${data.detail || data.message}`;
                queryResults.style.color = 'red';
            }
        } catch (error) {
            console.error('Error sending audio to backend:', error);
            queryResults.textContent = `Audio communication error: ${error.message}`;
            queryResults.style.color = 'red';
        }
    }
});
