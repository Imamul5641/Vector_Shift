# VectorShift Integrations Technical Assessment

Thank you for taking the time to interview with us at VectorShift! As part of the interview process, we would like you to complete an integrations technical assessment.

## Getting Started

You can find all files necessary for the assignment in the `/frontend/src` and `/backend` folders. Feel free to make any changes to the provided files, including:
- Adding new files
- Deleting existing files
- Installing new packages
- Modifying any provided code

### Technologies Used
- **Frontend:** JavaScript/React
- **Backend:** Python/FastAPI
- **Database:** Redis

### Running the Application
#### Frontend
Navigate to the `/frontend` directory and run:
```sh
npm i
npm run start
```

#### Backend
Navigate to the `/backend` directory and run:
```sh
uvicorn main:app --reload
```

#### Redis
Ensure that Redis is running by executing:
```sh
redis-server
```

If you have any questions, reach out to [recruiting@vectorshift.ai](mailto:recruiting@vectorshift.ai).

---

## Assessment Overview
The assessment consists of two parts:

### Part 1: HubSpot OAuth Integration

#### Backend
1. Navigate to the `/backend/integrations` folder.
2. You will find two completed files (`airtable.py` and `notion.py`) and one incomplete file (`hubspot.py`).
3. Complete the following functions in `hubspot.py`:
   - `authorize_hubspot`
   - `oauth2callback_hubspot`
   - `get_hubspot_credentials`
4. Use the structure of the completed integrations (`airtable.py` and `notion.py`) and relevant HubSpot documentation to guide your implementation.

#### Frontend
1. Navigate to `/frontend/src/integrations`.
2. You will find two existing integration files (`airtable.js` and `notion.js`) and an empty file for the HubSpot integration (`hubspot.js`).
3. Complete `hubspot.js`.
4. Integrate HubSpot into the UI by modifying the necessary files.

**Note:** The AirTable and Notion integrations will not work as the client information has been redacted. Create a **client ID** and **client secret** to test your HubSpot integration. Optionally, you can create your own Notion and AirTable app credentials for additional testing.

---

### Part 2: Loading HubSpot Items

#### Backend
1. Navigate to `/backend/integrations/hubspot.py`.
2. Complete the `get_items_hubspot` function.
3. This function should:
   - Query HubSpot’s API using credentials obtained from the OAuth flow.
   - Return a list of `IntegrationItem` objects.
   - Determine which fields and endpoints are most relevant for HubSpot (reference `notion.py` and `airtable.py`).

#### Frontend
1. Determine how to display the resulting list of **Integration Items**.
2. A simple approach is to print the final list to the console.

**Note:** Similar to Part 1, the AirTable and Notion integrations will not work as their client information has been redacted. Create a **client ID** and **client secret** to test your HubSpot integration.

---

## Submission
Once you have completed the assessment, submit your work as instructed by the recruiting team.

Good luck, and happy coding!
