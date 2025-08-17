document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dbUrlInput = document.getElementById('dbUrl');
    const connectDbButton = document.getElementById('connectDb');
    const connectionStatus = document.getElementById('connectionStatus');
    const naturalLanguageQuery = document.getElementById('naturalLanguageQuery');
    const executeQueryButton = document.getElementById('executeQuery');
    const startSpeechButton = document.getElementById('startSpeech');
    const stopSpeechButton = document.getElementById('stopSpeech');
    const queryResults = document.getElementById('queryResults');
    const dbSchemaDisplay = document.getElementById('dbSchema');

    // LLM config elements (provider only)
    const llmProvider = document.getElementById('llmProvider');
    
    // Tab elements
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Speech recognition variables
    let mediaRecorder;
    let audioChunks = [];
    let recognition;

    // Base URL for backend API
    const API_BASE_URL = '/api/v1';
    console.log('EasyQuery frontend running. API_BASE_URL =', API_BASE_URL);

    // Initialize tab functionality
    function initTabs() {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-tab');
                
                // Remove active class from all buttons and panes
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));
                
                // Add active class to clicked button and corresponding pane
                button.classList.add('active');
                document.getElementById(`${tabId}-tab`).classList.add('active');
            });
        });
    }

    // Helper function to update status message with appropriate styling
    function updateStatus(element, message, type) {
        element.textContent = message;
        // Remove all status classes
        element.classList.remove('success', 'error', 'warning', 'info');
        
        // Add appropriate class based on type
        if (type) {
            element.classList.add(type);
        }
    }

    // LLM config persistence (provider only)
    function loadLlmConfig() {
        try {
            const cfg = JSON.parse(localStorage.getItem('llmConfig') || '{}');
            if (cfg.provider && llmProvider) llmProvider.value = cfg.provider;
        } catch {}
    }
    
    function getLlmConfig() {
        return {
            provider: llmProvider ? llmProvider.value.trim() : ''
        };
    }
    
    if (llmProvider) {
        llmProvider.addEventListener('change', () => {
            const { provider } = getLlmConfig();
            localStorage.setItem('llmConfig', JSON.stringify({ provider }));
        });
    }

    // --- Database Connection ---
    connectDbButton.addEventListener('click', async () => {
        const dbUrl = dbUrlInput.value.trim();
        if (!dbUrl) {
            updateStatus(connectionStatus, 'Please enter a database URL.', 'error');
            return;
        }

        updateStatus(connectionStatus, 'Connecting...', 'info');

        try {
            const url = `${API_BASE_URL}/connection/connect`;
            console.log('Requesting', url);
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ db_url: dbUrl })
            });
            const data = await response.json();

            if (response.ok) {
                updateStatus(connectionStatus, `Connected to ${data.db_url}`, 'success');
                fetchSchema(); // Fetch schema on successful connection
            } else {
                updateStatus(connectionStatus, `Connection failed: ${data.detail || data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error connecting to database:', error);
            updateStatus(connectionStatus, `Connection error: ${error.message}`, 'error');
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
                dbSchemaDisplay.style.color = 'var(--danger-color)';
            }
        } catch (error) {
            console.error('Error fetching schema:', error);
            dbSchemaDisplay.textContent = `Error fetching schema: ${error.message}`;
            dbSchemaDisplay.style.color = 'var(--danger-color)';
        }
    }

    // --- Execute Text Query ---
    executeQueryButton.addEventListener('click', async () => {
        const queryText = naturalLanguageQuery.value.trim();
        if (!queryText) {
            updateStatus(queryResults, 'Please enter a query.', 'error');
            return;
        }

        const { provider } = getLlmConfig();
        if (!provider) {
            updateStatus(queryResults, 'Please configure LLM provider first.', 'error');
            return;
        }

        updateStatus(queryResults, 'Executing query...', 'info');

        try {
            const response = await fetch(`${API_BASE_URL}/query/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query_text: queryText, llm_provider: provider })
            });
            const data = await response.json();

            if (response.ok) {
                queryResults.textContent = JSON.stringify(data.results, null, 2);
                queryResults.style.color = 'var(--text-color, var(--dark-color))';
            } else {
                updateStatus(queryResults, `Query failed: ${data.detail || data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error executing query:', error);
            updateStatus(queryResults, `Query error: ${error.message}`, 'error');
        }
    });

    // --- Speech Recognition ---
    startSpeechButton.addEventListener('click', async () => {
        const { provider } = getLlmConfig();
        if (!provider) {
            updateStatus(queryResults, 'Please configure LLM provider first.', 'error');
            return;
        }

        startSpeechButton.disabled = true;
        stopSpeechButton.disabled = false;
        updateStatus(queryResults, 'Listening...', 'info');

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Check for supported MIME types
            let mimeType = 'audio/webm';
            if (!MediaRecorder.isTypeSupported('audio/webm')) {
                mimeType = 'audio/ogg';
                if (!MediaRecorder.isTypeSupported('audio/ogg')) {
                    mimeType = '';
                }
            }
            
            mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                // Use the same MIME type for the blob
                const audioBlob = new Blob(audioChunks, { type: mimeType || 'audio/webm' });
                await sendAudioToBackend(audioBlob);
                startSpeechButton.disabled = false;
                stopSpeechButton.disabled = true;
            };

            mediaRecorder.start();
        } catch (error) {
            console.error('Error accessing microphone:', error);
            updateStatus(queryResults, `Microphone access error: ${error.message}`, 'error');
            startSpeechButton.disabled = false;
            stopSpeechButton.disabled = true;
        }
    });

    stopSpeechButton.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            updateStatus(queryResults, 'Processing speech...', 'warning');
        }
    });

    async function sendAudioToBackend(audioBlob) {
        try {
            const formData = new FormData();
            // Use the actual MIME type of the blob for the filename
            const mimeType = audioBlob.type || 'audio/webm';
            const extension = mimeType.split('/')[1] || 'webm';
            formData.append('audio_file', audioBlob, `audio.${extension}`);

            const response = await fetch(`${API_BASE_URL}/query/speech-to-text`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                // Display the converted text in the textarea
                naturalLanguageQuery.value = data.text_query;
                updateStatus(queryResults, 'Speech converted to text. Review and click Execute Query to run.', 'success');
            } else {
                updateStatus(queryResults, `Speech conversion failed: ${data.detail || data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error sending audio to backend:', error);
            updateStatus(queryResults, `Audio communication error: ${error.message}`, 'error');
        }
    }

    // Initialize the application
    initTabs();
    loadLlmConfig();
});
