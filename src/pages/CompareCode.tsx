// import React, { useState } from "react";
// import { TextField, Button, Container, Typography, Box } from "@mui/material";
// import { AccountCircle, Email, Lock, Cake, Wc } from "@mui/icons-material";
// import TerminalIcon from "@mui/icons-material/Terminal";
// import GitHubIcon from "@mui/icons-material/GitHub";
// import AutoStoriesIcon from "@mui/icons-material/AutoStories";
// import Loader from "../components/Loader";

// const UserRegistrationForm: React.FC = () => {
//   const [formData, setFormData] = useState({
//     owner: "Biswanathdas1996",
//     repo: "agent-tool",
//     pr_number: "",
//     user_story: ``,
//   });

//   const [report, setReport] = useState<any>("");

//   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };
//   const [loading, setLoading] = useState(false);
//   const [fetchingPR, setFetchingPR] = useState(false);
//   const [prDetails, setPrDetails] = useState<any>(null);

//   const handleSubmit = async () => {
//     setLoading(true);
//     const myHeaders = new Headers();
//     myHeaders.append(
//       "Cookie",
//       "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzBmYzk0MmFmMjUzOGEyZWI0Zjg5NDIiLCJlbWFpbCI6IjQ0NmhpaUBnbWFpbC5jb20iLCJpc0FkbWluIjpmYWxzZSwiaWF0IjoxNzI5MDk0MTU5LCJleHAiOjE3MjkwOTc3NTl9.erRyF3fH52Islq5z5Bf0zJLWjrbszs_m5vObPomw1kw"
//     );
//     myHeaders.append("Content-Type", "application/json");

//     const raw = JSON.stringify(formData);

//     const requestOptions: RequestInit = {
//       method: "POST",
//       headers: myHeaders,
//       body: raw,
//       redirect: "follow",
//     };

//     try {
//       const response = await fetch(
//         "http://localhost:5000/compare-user-story-code",
//         requestOptions
//       );
//       const result = await response.json();
//       console.log(result);
//       setReport(result);
//       setLoading(false);
//     } catch (error) {
//       console.error("Error:", error);
//       setLoading(false);
//     }
//   };

//   const fetchPullRequestDetails = async () => {
//     setFetchingPR(true);
//     try {
//       const response = await fetch(
//         `https://api.github.com/repos/${formData.owner}/${formData.repo}/pulls`
//       );
//       const prDetails = await response.json();
//       console.log(prDetails);

//       const prData = prDetails.map((pr: any) => ({
//         number: pr.number,
//         title: pr.title,
//       }));

//       setPrDetails(prData);
//       setFetchingPR(false);
//     } catch (error) {
//       console.error("Error fetching PR details:", error);
//       setFetchingPR(false);
//     }
//   };

//   React.useEffect(() => {
//     fetchPullRequestDetails();
//   }, []);

//   React.useEffect(() => {
//     fetchPullRequestDetails();
//   }, [formData.owner, formData.repo]);

//   return (
//     <>
//       <h2 style={{ marginBottom: 0 }}>Compare code </h2>
//       <span style={{ marginBottom: 20, fontSize: 11 }}>
//         Sample repo: <b>https://github.com/Biswanathdas1996/agent-tool/pulls</b>
//       </span>
//       <br />
//       <br />
//       <Container>
//         <Typography variant="h4" gutterBottom></Typography>
//         <Box display="flex" flexDirection="column" gap={2}>
//           <TextField
//             label="Repository Owner"
//             name="owner"
//             onChange={handleChange}
//             value={formData.owner}
//             InputProps={{
//               startAdornment: <AccountCircle style={{ marginRight: 10 }} />,
//             }}
//           />
//           <TextField
//             label="Repository Name"
//             name="repo"
//             value={formData.repo}
//             onChange={handleChange}
//             InputProps={{
//               startAdornment: <GitHubIcon style={{ marginRight: 10 }} />,
//             }}
//           />
//           {fetchingPR ? (
//             <Loader showIcon={false} text="Fetching PR List" />
//           ) : (
//             <TextField
//               select
//               label="Pull Request Number"
//               value={formData.pr_number}
//               name="pr_number"
//               onChange={handleChange}
//               InputProps={{
//                 startAdornment: <TerminalIcon style={{ marginRight: 10 }} />,
//               }}
//               SelectProps={{
//                 native: true,
//               }}
//             >
//               <option value="">Select Pull Request Number</option>
//               {prDetails &&
//                 prDetails.map((pr: any) => (
//                   <option key={pr.number} value={pr.number}>
//                     {pr.title}
//                   </option>
//                 ))}
//             </TextField>
//           )}

//           <TextField
//             type="textarea"
//             label="User Story"
//             name="user_story"
//             value={formData.user_story}
//             onChange={handleChange}
//             InputProps={{
//               startAdornment: <AutoStoriesIcon style={{ marginRight: 10 }} />,
//             }}
//             multiline
//             rows={10}
//           />
//           {loading ? (
//             <Loader showIcon={false} />
//           ) : (
//             <Button variant="contained" color="warning" onClick={handleSubmit}>
//               Submit
//             </Button>
//           )}
//         </Box>
//       </Container>
//       <div style={{ margin: "2rem", background: "#f1f1f1", padding: 15 }}>
//         <div dangerouslySetInnerHTML={{ __html: report?.result }} />
//       </div>
//     </>
//   );
// };

// export default UserRegistrationForm;

import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Container,
  Typography,
  Box,
  MenuItem,
} from "@mui/material";
import { AccountCircle, Terminal, GitHub } from "@mui/icons-material";
import Loader from "../components/Loader";

const userStories = [
  {
    label: "Select User Story",
    value: `
    `,
  },
  {
    label: "EMI Loan Calculation",
    value: `Feature: EMI Calculator

    Scenario: Calculate EMI for different loan types
    
    Given the user is on the EMI calculator page
    And the user selects "Home Loan" as the loan type
    And the user enters a loan amount of 1000000
    And the user enters an interest rate of 8.5
    And the user enters a loan tenure of 20 years
    When the user clicks the "Calculate" button
    Then the EMI should be calculated and displayed accurately
    
    And the user selects "Car Loan" as the loan type
    And the user enters a loan amount of 500000
    And the user enters an interest rate of 9.2
    And the user enters a loan tenure of 5 years
    When the user clicks the "Calculate" button
    Then the EMI should be calculated and displayed accurately
    
    And the user selects "Business Loan" as the loan type
    And the user enters a loan amount of 2000000
    And the user enters an interest rate of 10.5
    And the user enters a loan tenure of 10 years
    When the user clicks the "Calculate" button
    Then the EMI should be calculated and displayed accurately
    
    And the user selects "Personal Loan" as the loan type
    And the user enters a loan amount of 100000
    And the user enters an interest rate of 12
    And the user enters a loan tenure of 3 years
    When the user clicks the "Calculate" button
    Then the EMI should be calculated and displayed accurately
    
    
    Scenario Outline: Error Handling for Invalid Inputs
    
    Given the user is on the EMI calculator page
    And the user selects "<Loan Type>" as the loan type
    And the user enters a loan amount of <Loan Amount>
    And the user enters an interest rate of <Interest Rate>
    And the user enters a loan tenure of <Loan Tenure>
    When the user clicks the "Calculate" button
    Then an appropriate error message should be displayed
    
    Examples:
    | Loan Type | Loan Amount | Interest Rate | Loan Tenure |
    |---------------|-------------|---------------|-------------|
    | Home Loan | -1000000 | 8.5 | 20 |
    | Car Loan | 500000 | -9.2 | 5 |
    | Business Loan | 2000000 | 10.5 | -10 |
    | Personal Loan | 100000 | 12 | 0 |
    | Home Loan | abc | 8.5 | 20 |
    | Car Loan | 500000 | xyz | 5 |
    
    
    Acceptance Criteria:
    
    The calculator should accurately compute EMIs for Home Loans, Car Loans, Business Loans, and Personal Loans using standard EMI calculation formulas.
    The calculator should handle invalid inputs (negative numbers, non-numeric values, zero tenure) gracefully, displaying informative error messages to the user.
    The calculated EMI should be displayed clearly and prominently to the user.
    The UI should be intuitive and user-friendly.
    The calculator should be responsive across different screen sizes.
    
    
    Assumptions:
    
    The EMI calculation will use the standard formula: EMI = [P x R x (1+R)^N] / [(1+R)^N-1] where P is the principal loan amount, R is the monthly interest rate (annual interest rate/12), and N is the loan tenure in months.
    The user will input valid numerical data for Loan Amount, Interest Rate, and Loan Tenure. Error handling is in place for invalid inputs as described in the acceptance criteria.
    The application provides a user interface (UI) for input and output.
    
    
    Dependencies:
    
    A backend service or API to handle the EMI calculation. (If the calculation is not done client-side.)
    A database (if storing user input data is required).
    A UI framework (React, Angular, etc. if applicable).
    `,
  },
];

const UserRegistrationForm: React.FC = () => {
  const [formData, setFormData] = useState({
    owner: "rrt270899",
    repo: "Emi-Calculator",
    pr_number: "",
    user_story: userStories[0].value, // Default to the first story
  });

  const [report, setReport] = useState<any>("");
  const [loading, setLoading] = useState(false);
  const [fetchingPR, setFetchingPR] = useState(false);
  const [prDetails, setPrDetails] = useState<any>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUserStoryChange = (
    event: React.ChangeEvent<{ value: unknown }>
  ) => {
    const selectedStory = userStories.find(
      (story) => story.value === event.target.value
    );
    setFormData({
      ...formData,
      user_story: selectedStory ? selectedStory.value : "",
    });
  };

  const handleSubmit = async () => {
    setLoading(true);

    const requestOptions: RequestInit = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };

    try {
      const response = await fetch(
        "http://localhost:5000/compare-user-story-code",
        requestOptions
      );
      const result = await response.json();
      setReport(result);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPullRequestDetails = async () => {
    setFetchingPR(true);
    try {
      const response = await fetch(
        `https://api.github.com/repos/${formData.owner}/${formData.repo}/pulls`
      );
      // const response = await fetch(
      //   `https://api.github.com/repos/${formData.owner}/${formData.repo}/pulls`,
      //   {
      //     headers: {
      //       Accept: "application/vnd.github.v3+json",
      //     },
      //   }
      // );
      const prData = await response.json();

      setPrDetails(
        prData.map((pr: any) => ({
          number: pr.number,
          title: pr.title,
        }))
      );
    } catch (error) {
      console.error("Error fetching PR details:", error);
    } finally {
      setFetchingPR(false);
    }
  };

  useEffect(() => {
    fetchPullRequestDetails();
  }, [formData.owner, formData.repo]);

  return (
    <>
      <h2 style={{ marginBottom: 0 }}>Compare Code</h2>
      <span style={{ marginBottom: 20, fontSize: 11 }}>
        Sample repo: <b>https://github.com/rrt270899/Emi-calculator/pulls</b>
      </span>
      <br />
      <br />
      <Container>
        <Typography variant="h4" gutterBottom></Typography>
        <Box display="flex" flexDirection="column" gap={2}>
          {/* Repository Owner */}
          <TextField
            label="Repository Owner"
            name="owner"
            onChange={handleChange}
            value={formData.owner}
            InputProps={{
              startAdornment: <AccountCircle style={{ marginRight: 10 }} />,
            }}
          />

          {/* Repository Name */}
          <TextField
            label="Repository Name"
            name="repo"
            value={formData.repo}
            onChange={handleChange}
            InputProps={{
              startAdornment: <GitHub style={{ marginRight: 10 }} />,
            }}
          />

          {/* Pull Request Dropdown */}
          {fetchingPR ? (
            <Loader showIcon={false} text="Fetching PR List" />
          ) : (
            <TextField
              select
              label="Pull Request Number"
              value={formData.pr_number}
              name="pr_number"
              onChange={handleChange}
              InputProps={{
                startAdornment: <Terminal style={{ marginRight: 10 }} />,
              }}
              SelectProps={{
                native: true,
              }}
            >
              <option value="">Select Pull Request Number</option>
              {prDetails &&
                prDetails.map((pr: any) => (
                  <option key={pr.number} value={pr.number}>
                    {pr.title}
                  </option>
                ))}
            </TextField>
          )}

          {/* User Story Dropdown */}
          <TextField
            select
            label="Select User Story"
            name="user_story"
            value={formData.user_story}
            onChange={handleUserStoryChange}
          >
            {userStories.map((story) => (
              <MenuItem key={story.label} value={story.value}>
                {story.label}
              </MenuItem>
            ))}
          </TextField>

          {/* Submit Button */}
          {loading ? (
            <Loader showIcon={false} />
          ) : (
            <Button variant="contained" color="warning" onClick={handleSubmit}>
              Submit
            </Button>
          )}
        </Box>
      </Container>

      {/* Display the Report */}
      <div style={{ margin: "2rem", background: "#f1f1f1", padding: 15 }}>
        <div dangerouslySetInnerHTML={{ __html: report?.result }} />
      </div>
    </>
  );
};

export default UserRegistrationForm;
