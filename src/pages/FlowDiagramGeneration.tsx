import React, { useState } from "react";
import FlowDiagram from "../components/FlowDiagram";
import { TextField, Button, Card } from "@mui/material";
import { useFetch } from "../hook/useFetch";
import { GENERATE_FLOW_CHART } from "../config";
import Loader from "../components/Loader";

const FlowDiagramGeneration: React.FC = () => {
  const [inputText, setInputText] = useState("");
  const [loadingUi, setLoadingUi] = useState(false);
  const [responseData, setResponseData] = useState<any>(null);
  const fetchData = useFetch();

  const handleSubmit = () => {
    setLoadingUi(true);
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
        <textarea
          style={{
            width: "95%",
            margin: "10px 0",
            padding: "10px",
            fontSize: "16px",
            borderRadius: "4px",
            border: "1px solid #ccc",
            resize: "vertical",
          }}
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

      <Card style={{ padding: 20, marginTop: 20, border: "1px solid #ccc" }}>
        {loadingUi ? (
          <Loader showIcon={false} />
        ) : (
          <FlowDiagram renderJson={responseData} />
        )}
      </Card>
    </div>
  );
};

export default FlowDiagramGeneration;
