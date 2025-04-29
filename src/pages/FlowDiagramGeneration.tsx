import React, { useState } from "react";
import FlowDiagram from "../components/FlowDiagram";
import { TextField, Button, Card } from "@mui/material";
import { useFetch } from "../hook/useFetch";
import { GENERATE_FLOW_CHART } from "../config";

const FlowDiagramGeneration: React.FC = () => {
  const [inputText, setInputText] = useState("");
  const [loadingUi, setLoadingUi] = useState(false);
  const [responseData, setResponseData] = useState<any>(null);
  const fetchData = useFetch();

  const handleSubmit = () => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      description: inputText,
      sql_query: inputText,
    });

    const requestOptions: RequestInit = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow" as RequestRedirect,
    };

    fetchData(GENERATE_FLOW_CHART, requestOptions)
      .then((response) => response.json())
      .then((result) => {
        setResponseData(result);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setLoadingUi(false);
      });
  };
  return (
    <div>
      <h2>Flow Diagram Generation</h2>

      <>
        <TextField
          label="Enter text"
          variant="outlined"
          fullWidth
          margin="normal"
          multiline
          rows={4}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <Button variant="contained" color="warning" onClick={handleSubmit}>
          Submit
        </Button>
        <Button
          variant="outlined"
          color="warning"
          style={{ marginLeft: 10 }}
          onClick={() => setResponseData(null)}
        >
          Clear
        </Button>
      </>

      {responseData && (
        <Card style={{ padding: 20, marginTop: 20, border: "1px solid #ccc" }}>
          <FlowDiagram renderJson={responseData} />
        </Card>
      )}
    </div>
  );
};

export default FlowDiagramGeneration;
