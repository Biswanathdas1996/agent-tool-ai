import React, { useState, useEffect } from "react";
import {
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import { HTML_UPLOAD } from "../config";
import { AlertColor } from "@mui/material/Alert";
import { useFetch } from "../hook/useFetch";
import ReactJson from "react-json-view";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";

const fetchData = useFetch();
const HtmlUpload = () => {
  const [htmlContent, setHtmlContent] = useState("");
  const [url, setUrl] = useState("https://www.servicedogregistration.org");
  const [inputType, setInputType] = useState(""); // Start with an empty string
  const [responseData, setResponseData] = useState<any>(null);
  const [alertMessage, setAlertMessage] = useState<string | null>(null);
  const [alertSeverity, setAlertSeverity] = useState<AlertColor>("success");
  const [loading, setLoading] = useState(false);

  const [value, setValue] = React.useState("1");

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();

    if (inputType === "") {
      setAlertMessage("Please select an input type");
      setAlertSeverity("warning");
      return;
    }

    try {
      setLoading(true);
      const response = await fetchData(`${HTML_UPLOAD}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ html: htmlContent, url: url }),
      });

      if (!response.ok) {
        setLoading(false);
        setAlertMessage("Error");
        setAlertSeverity("error");
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setLoading(false);
      setAlertMessage("Generated successfully");
      setAlertSeverity("success");
      setResponseData(data);
    } catch (error) {
      setLoading(false);
      setAlertMessage("Error");
      setAlertSeverity("error");
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    if (alertMessage) {
      const timer = setTimeout(() => {
        setAlertMessage(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [alertMessage]);

  return (
    <div style={{ padding: "20px" }}>
      <h2>HTML Upload</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        {alertMessage && (
          <Alert
            severity={alertSeverity}
            onClose={() => setAlertMessage(null)}
            style={{ position: "fixed", zIndex: 1, top: "11%", right: "3%" }}
          >
            {alertMessage}
          </Alert>
        )}

        <FormControl fullWidth style={{ marginBottom: "10px" }}>
          <Select
            value={inputType}
            onChange={(e) => setInputType(e.target.value)}
            displayEmpty
          >
            <MenuItem value="">
              <em>Select an option</em>
            </MenuItem>
            <MenuItem value="html">HTML</MenuItem>
            <MenuItem value="url">URL</MenuItem>
          </Select>
        </FormControl>

        {inputType === "html" && (
          <TextField
            label="HTML Source Code"
            multiline
            rows={10}
            variant="outlined"
            fullWidth
            value={htmlContent}
            onChange={(e) => {
              setHtmlContent(e.target.value);
              setUrl("");
            }}
            style={{ marginBottom: "10px" }}
          />
        )}

        {inputType === "url" && (
          <TextField
            label="URL"
            variant="outlined"
            fullWidth
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setHtmlContent("");
            }}
            style={{ marginBottom: "10px" }}
          />
        )}

        <Button
          type="submit"
          style={{ backgroundColor: "#d04a02" }}
          variant="contained"
          color="primary"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Submit"}
        </Button>
      </form>

      {responseData && (
        <div>
          <Box sx={{ width: "100%", typography: "body1" }}>
            <TabContext value={value}>
              <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                <TabList
                  onChange={handleChange}
                  aria-label="lab API tabs example"
                >
                  <Tab label="Input Elements" value="1" />
                  <Tab label="Media Elements" value="2" />
                  <Tab label="Text Elements" value="3" />
                </TabList>
              </Box>
              <TabPanel value="1">
                {responseData && (
                  <ReactJson
                    src={responseData?.form_elements}
                    theme="monokai"
                  />
                )}
              </TabPanel>
              <TabPanel value="2">
                {" "}
                {responseData && (
                  <ReactJson
                    src={responseData?.media_elements}
                    theme="monokai"
                  />
                )}
              </TabPanel>
              <TabPanel value="3">
                {" "}
                {responseData && (
                  <ReactJson
                    src={responseData?.text_elements}
                    theme="monokai"
                  />
                )}
              </TabPanel>
            </TabContext>
          </Box>
        </div>
      )}
    </div>
  );
};

export default HtmlUpload;
