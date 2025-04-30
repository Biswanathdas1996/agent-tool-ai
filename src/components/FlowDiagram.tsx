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

import "reactflow/dist/style.css";

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
  return (
    <div style={{ height: 500, width: "100%" }}>
      <button
        onClick={() => {
          const reactFlowWrapper = document.querySelector(
            ".react-flow"
          ) as HTMLElement;
          if (reactFlowWrapper) {
            import("html-to-image").then((htmlToImage) => {
              htmlToImage.toPng(reactFlowWrapper).then((dataUrl) => {
                const link = document.createElement("a");
                link.download = "flow-diagram.png";
                link.href = dataUrl;
                link.click();
              });
            });
          }
        }}
        style={{
          marginBottom: "10px",
          padding: "8px 16px",
          backgroundColor: "#007acc",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Download as PNG
      </button>
      <ReactFlow
        nodes={nodesState.map((node) => ({
          ...node,
          style: {
            ...node.style,
            backgroundColor: "#f0f8ff", // Light blue background
            border: "2px solid #007acc", // Blue border
            borderRadius: "5px", // Rounded corners
            color: "#333", // Text color
            fontWeight: "bold", // Bold text
          },
        }))}
        edges={edgesState.map((edge) => ({
          ...edge,
          type: "straight", // Change to "straight" for curved edges
          markerEnd: {
            type: MarkerType.ArrowClosed, // Use the correct MarkerType enum
            color: "#007acc", // Arrow color
          },
        }))}
        fitView
        nodesDraggable
        onNodesChange={(changes) => {
          changes.forEach((change) => {
            if (change.type === "select" && change.selected) {
              const nodeToUpdate = nodesState.find(
                (node) => node.id === change.id
              );
              if (nodeToUpdate) {
                const newLabel = prompt(
                  "Enter new label:",
                  nodeToUpdate.data?.label || ""
                );
                if (newLabel !== null) {
                  setNodesState((nds) =>
                    nds.map((node) =>
                      node.id === nodeToUpdate.id
                        ? { ...node, data: { ...node.data, label: newLabel } }
                        : node
                    )
                  );
                }
              }
            }
          });
        }}
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
            type: "straight", // Change to "straight" for curved edges
            label: prompt("Enter label for the new connection:", "") || "",
            labelBgStyle: {
              fill: "#fff",
              color: "#222",
              strokeWidth: 1,
              stroke: "#222",
            },
            labelStyle: { fontWeight: 700 },
            markerEnd: {
              type: "arrowclosed", // Add arrow to indicate direction
              width: 20,
              height: 20,
              color: "#007acc", // Arrow color
            },
          };
          setEdgesState((eds) => addEdge(newEdge, eds));
        }}
        connectionMode={ConnectionMode.Loose} // Allow connecting any node
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default FlowDiagram;
