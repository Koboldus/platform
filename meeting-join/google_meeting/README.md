### Zoom Meeting Join Script

Welcome to the Google Meeting Join Script repository! This folder contains sample scripts designed to demonstrate the utilization of the `/asr/meeting/join` API for seamlessly joining Google meetings.

#### Instructions:

To effectively run the `google_meeting_join.py` script, please follow these steps:

1. **Replace JWT Token**: 
   Ensure to replace the placeholder JWT token with your own generated JWT token. This token is crucial for authenticating the Voicegain API. If you do not have a JWT token, then follow this article to generate it:
   https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication

2. **Install Python Packages**: 
   Install the Python requests module using the below command:
   ```bash
   pip install requests==2.31.0
   ```

3. **Replace Meeting Link**: 
   Substitute the placeholder Google meeting link (`meetingUrl`) with the actual invitation link of the ongoing Google meeting that you intend to join.

4. **Start the Google Meeting**: 
   If the Google meeting is not yet initiated, please start it before executing the script.

#### Running the Script:

Once you've completed the above steps, navigate to the directory containing the script in your terminal and execute the following command:

```bash
python google_meeting_join.py
```
