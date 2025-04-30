// FlowDiagram.jsx
import React, { useState } from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  ConnectionMode,
  MarkerType,
} from "reactflow";
import ReactJson from "react-json-view";
import "reactflow/dist/style.css";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";

interface FlowDiagramProps {
  renderJson: any; // Replace 'any' with the appropriate type if known
}

const FlowDiagram = ({ renderJson }: FlowDiagramProps) => {
  if (!renderJson) {
    return <div>No data available to render the flow diagram.</div>;
  }
  const { nodes, edges } = renderJson;
  const [nodesState, setNodesState] = useNodesState(nodes);
  const [edgesState, setEdgesState] = useEdgesState(edges);
  const [value, setValue] = React.useState("1");

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };

  return (
    <>
      <Box
        sx={{
          width: "100%",
          typography: "body1",

          maxHeight: "100vh",
          zIndex: 1000,
        }}
      >
        <TabContext value={value}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <TabList onChange={handleChange} aria-label="lab API tabs example">
              <Tab label="Diagram" value="1" />
              <Tab label="JSON" value="2" />
            </TabList>
          </Box>
          <TabPanel value="1" sx={{ overflow: "auto", maxHeight: "80vh" }}>
            <div style={{ height: 500, overflow: "hidden" }}>
              <ReactFlow
                nodes={nodesState.map((node) => ({
                  ...node,
                  style: {
                    ...(node.style || {}),
                    backgroundColor: "#f0f8ff",
                    border: "2px solid #007acc",
                    borderRadius: "5px",
                    color: "#333",
                    fontWeight: "bold",
                  },
                }))}
                edges={edgesState.map((edge) => ({
                  ...edge,
                  type: "straight",
                  markerEnd: {
                    type: MarkerType.ArrowClosed,
                    color: "#007acc",
                  },
                }))}
                fitView
                nodesDraggable
                onEdgesChange={(changes) => {
                  changes.forEach((change) => {
                    if (change.type === "select" && change.selected) {
                      const edgeToUpdate = edgesState.find(
                        (edge) => edge.id === change.id
                      );
                      if (edgeToUpdate) {
                        const newLabel = prompt(
                          "Enter new label for the edge:",
                          typeof edgeToUpdate.label === "string"
                            ? edgeToUpdate.label
                            : ""
                        );
                        if (newLabel !== null) {
                          setEdgesState((eds) =>
                            eds.map((edge) =>
                              edge.id === edgeToUpdate.id
                                ? { ...edge, label: newLabel }
                                : edge
                            )
                          );
                        }
                      }
                    }
                  });
                }}
                onConnect={(connection) => {
                  const newEdge = {
                    ...connection,
                    type: "straight",
                    label:
                      prompt("Enter label for the new connection:", "") || "",
                    labelBgStyle: {
                      fill: "#fff",
                      color: "#222",
                      strokeWidth: 1,
                      stroke: "#222",
                    },
                    labelStyle: { fontWeight: 700 },
                    markerEnd: {
                      type: "arrowclosed",
                      width: 20,
                      height: 20,
                      color: "#007acc",
                    },
                  };
                  setEdgesState((eds) => addEdge(newEdge, eds));
                }}
                connectionMode={ConnectionMode.Loose}
              >
                <MiniMap />
                <Controls />
                <Background />
              </ReactFlow>
            </div>
          </TabPanel>
          <TabPanel value="2" sx={{ overflow: "auto", maxHeight: "80vh" }}>
            <ReactJson
              src={renderJson}
              theme="rjv-default"
              onEdit={(edit) => {
                const { updated_src } = edit;
                const { nodes = [], edges = [] } = updated_src as {
                  nodes: any[];
                  edges: any[];
                };
                setNodesState((prevNodes) => [...prevNodes, ...nodes]);
                setEdgesState((prevEdges) => [...prevEdges, ...edges]);
              }}
              onAdd={(add) => {
                const { updated_src } = add;
                const { nodes = [], edges = [] } = updated_src as {
                  nodes: any[];
                  edges: any[];
                };
                setNodesState(nodes);
                setEdgesState(edges);
              }}
              onDelete={(del) => {
                const { updated_src } = del;
                const { nodes = [], edges = [] } = updated_src as {
                  nodes: any[];
                  edges: any[];
                };
                setNodesState(nodes);
                setEdgesState(edges);
              }}
            />
          </TabPanel>
        </TabContext>
      </Box>
    </>
  );
};

export default FlowDiagram;
