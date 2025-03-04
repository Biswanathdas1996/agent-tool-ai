import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  Button,
  MenuItem,
  Select,
  TextField,
  FormControl,
  Card,
} from "@mui/material";
import { countryData } from "../data/country";
import ReactJson from "react-json-view";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import Loader from "../components/Loader";

const GenerateSwiftData: React.FC = () => {
  const [type, setType] = useState("");
  const [sourceCountry, setSourceCountry] = useState("");
  const [destinationCountry, setDestinationCountry] = useState("");
  const [numberOfRecords, setNumberOfRecords] = useState("20");
  const [tableData, setTableData] = useState<any[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [value, setValue] = React.useState("1");
  const [loading, setLoading] = useState(false);
  const handleChange = (_event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };
  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSubmit = () => {
    setLoading(true);
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      type,
      source_country: sourceCountry,
      destination_country: destinationCountry,
      Number_Of_Records: Number(numberOfRecords),
    });

    const requestOptions: RequestInit = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow" as RequestRedirect,
    };

    fetch("http://127.0.0.1:5000/generate", requestOptions)
      .then((response) => response.json())
      .then((result) => {
        setTableData(result);
        localStorage.setItem("tableData", JSON.stringify(result));
      })
      .catch((error) => console.log("error", error))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    const storedData = localStorage.getItem("tableData");
    if (storedData) {
      setTableData(JSON.parse(storedData));
    }
  }, []);

  return (
    <div>
      <h2>Data Generation</h2>
      <Card
        style={{ margin: "4rem", padding: "2rem", background: "#80808030" }}
      >
        <FormControl fullWidth margin="normal">
          <label style={{ color: "black" }}>Type</label>
          <Select
            value={type}
            onChange={(e) => setType(e.target.value)}
            style={{ background: "white" }}
          >
            <MenuItem value="MT103">Customer Payments and Cheques</MenuItem>
            <MenuItem value="MT202">Financial Institution Transfers</MenuItem>
            <MenuItem value="MT300">Foreign Exchange and Money Market</MenuItem>
            <MenuItem value="MT540">
              Securities and Investment Transactions
            </MenuItem>
            <MenuItem value="MT700">Bill of Exchange and Guarantees</MenuItem>
            {/* Add more options as needed */}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <label style={{ color: "black" }}>Source Country</label>
          <Select
            value={sourceCountry}
            onChange={(e) => setSourceCountry(e.target.value)}
            native={false}
            renderValue={(selected) => selected}
            style={{ background: "white" }}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {countryData.map((country) => (
              <MenuItem key={country} value={country}>
                {country}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <label style={{ color: "black" }}>Destination Country</label>
          <Select
            value={destinationCountry}
            onChange={(e) => setDestinationCountry(e.target.value)}
            native={false}
            renderValue={(selected) => selected}
            style={{ background: "white" }}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {countryData.map((country) => (
              <MenuItem key={country} value={country}>
                {country}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <label style={{ color: "black" }}>Number of Records</label>
          <TextField
            type="number"
            value={numberOfRecords}
            onChange={(e) => setNumberOfRecords(e.target.value)}
            style={{ background: "white" }}
          />
        </FormControl>
        <br />
        <Button
          variant="contained"
          color="warning"
          size="large"
          onClick={handleSubmit}
        >
          Generate
        </Button>
      </Card>
      <br />
      <br />
      {loading ? (
        <Loader showIcon={false} />
      ) : (
        <>
          {tableData && tableData.length > 0 && (
            <Card>
              <Box sx={{ width: "100%", typography: "body1" }}>
                <TabContext value={value}>
                  <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                    <TabList
                      onChange={handleChange}
                      aria-label="lab API tabs example"
                    >
                      <Tab label="Table" value="1" />
                      <Tab label="JSON" value="2" />
                    </TabList>
                  </Box>
                  <TabPanel value="1">
                    {" "}
                    <TableContainer component={Paper}>
                      <Table>
                        <TableHead>
                          <TableRow
                            style={{ backgroundColor: "rgb(239 108 0 / 78%)" }}
                          >
                            {tableData.length > 0 &&
                              Object.keys(tableData[0].swift)
                                .sort((a, b) => {
                                  const aIsString =
                                    typeof tableData[0].swift[a] === "string";
                                  const bIsString =
                                    typeof tableData[0].swift[b] === "string";
                                  return aIsString === bIsString
                                    ? 0
                                    : aIsString
                                    ? -1
                                    : 1;
                                })
                                .map((key) => (
                                  <TableCell
                                    key={key}
                                    style={{
                                      background: "rgb(237 108 2)",
                                      color: "white",
                                      whiteSpace: "nowrap",
                                    }}
                                    align={
                                      typeof tableData[0].swift[key] ===
                                      "number"
                                        ? "right"
                                        : "left"
                                    }
                                  >
                                    {key
                                      .replace(/([A-Z])/g, " $1")
                                      .trim()
                                      .replace(/^./, (str) =>
                                        str.toUpperCase()
                                      )}
                                  </TableCell>
                                ))}
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {tableData
                            .slice(
                              page * rowsPerPage,
                              page * rowsPerPage + rowsPerPage
                            )
                            .map((data: any, index: number) => (
                              <TableRow
                                key={index}
                                style={{
                                  backgroundColor:
                                    index % 2 === 0 ? "#f5f5f5" : "white",
                                }}
                              >
                                {Object.keys(data.swift)
                                  .sort((a, b) => {
                                    const aIsString =
                                      typeof data.swift[a] === "string";
                                    const bIsString =
                                      typeof data.swift[b] === "string";
                                    return aIsString === bIsString
                                      ? 0
                                      : aIsString
                                      ? -1
                                      : 1;
                                  })
                                  .map((key, i) => (
                                    <TableCell
                                      key={i}
                                      align={
                                        typeof data.swift[key] === "number"
                                          ? "right"
                                          : "left"
                                      }
                                      style={{
                                        minWidth: "150px",
                                        whiteSpace: "nowrap",
                                      }}
                                    >
                                      {typeof data.swift[key] === "object" &&
                                      data.swift[key] !== null ? (
                                        <TableContainer component={Paper}>
                                          <Table size="small">
                                            <TableBody>
                                              {Object.entries(
                                                data.swift[key]
                                              ).map(
                                                (
                                                  [nestedKey, nestedValue],
                                                  nestedIndex
                                                ) => (
                                                  <TableRow key={nestedIndex}>
                                                    <TableCell>
                                                      {nestedKey}
                                                    </TableCell>
                                                    <TableCell>
                                                      {typeof nestedValue ===
                                                        "object" &&
                                                      nestedValue !== null
                                                        ? JSON.stringify(
                                                            nestedValue
                                                          )
                                                        : String(nestedValue)}
                                                    </TableCell>
                                                  </TableRow>
                                                )
                                              )}
                                            </TableBody>
                                          </Table>
                                        </TableContainer>
                                      ) : (
                                        String(data.swift[key])
                                      )}
                                    </TableCell>
                                  ))}
                              </TableRow>
                            ))}
                        </TableBody>
                      </Table>
                      <TablePagination
                        rowsPerPageOptions={[5, 10, 25]}
                        component="div"
                        count={tableData.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                      />
                    </TableContainer>
                  </TabPanel>
                  <TabPanel value="2">
                    {" "}
                    {tableData && tableData.length > 0 && (
                      <ReactJson src={tableData} theme="monokai" />
                    )}
                  </TabPanel>
                </TabContext>
              </Box>
            </Card>
          )}
        </>
      )}
    </div>
  );
};

export default GenerateSwiftData;
