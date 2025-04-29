// FlowDiagram.jsx
import React, { useState } from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from "reactflow";

import "reactflow/dist/style.css";

// const flowData = {
//   nodes: [
//     {
//       id: "start",
//       type: "input",
//       data: {
//         label: "Do you understand flowcharts?",
//       },
//       position: {
//         x: 0,
//         y: 0,
//       },
//     },
//     {
//       id: "yes_understand",
//       data: {
//         label: "Great! Visit the Diagram Community for examples and templates.",
//       },
//       position: {
//         x: 300,
//         y: 0,
//       },
//     },
//     {
//       id: "no_understand",
//       data: {
//         label: "Would you like to start with the basics?",
//       },
//       position: {
//         x: 0,
//         y: 200,
//       },
//     },
//     {
//       id: "yes_basics",
//       data: {
//         label: "Read a complete flowchart guide with examples.",
//       },
//       position: {
//         x: 300,
//         y: 200,
//       },
//     },
//     {
//       id: "no_basics",
//       data: {
//         label: "Read more about flowcharts.",
//       },
//       position: {
//         x: 300,
//         y: 400,
//       },
//     },
//     {
//       id: "end1",
//       type: "output",
//       data: {
//         label: "End",
//       },
//       position: {
//         x: 600,
//         y: 0,
//       },
//     },
//     {
//       id: "end2",
//       type: "output",
//       data: {
//         label: "End",
//       },
//       position: {
//         x: 600,
//         y: 200,
//       },
//     },
//     {
//       id: "end3",
//       type: "output",
//       data: {
//         label: "End",
//       },
//       position: {
//         x: 600,
//         y: 400,
//       },
//     },
//   ],
//   edges: [
//     {
//       id: "e1-2",
//       source: "start",
//       target: "yes_understand",
//       label: "Yes",
//       labelBgStyle: {
//         fill: "#fff",
//         color: "#222",
//         strokeWidth: 1,
//         stroke: "#222",
//       },
//       labelStyle: { fontWeight: 700 },
//     },
//     {
//       id: "e1-3",
//       source: "start",
//       target: "no_understand",
//       label: "No",
//       labelBgStyle: {
//         fill: "#fff",
//         color: "#222",
//         strokeWidth: 1,
//         stroke: "#222",
//       },
//       labelStyle: { fontWeight: 700 },
//     },
//     {
//       id: "e3-4",
//       source: "no_understand",
//       target: "yes_basics",
//       label: "Yes",
//       labelBgStyle: {
//         fill: "#fff",
//         color: "#222",
//         strokeWidth: 1,
//         stroke: "#222",
//       },
//       labelStyle: { fontWeight: 700 },
//     },
//     {
//       id: "e3-5",
//       source: "no_understand",
//       target: "no_basics",
//       label: "No",
//       labelBgStyle: {
//         fill: "#fff",
//         color: "#222",
//         strokeWidth: 1,
//         stroke: "#222",
//       },
//       labelStyle: { fontWeight: 700 },
//     },
//     {
//       id: "e2-6",
//       source: "yes_understand",
//       target: "end1",
//     },
//     {
//       id: "e4-7",
//       source: "yes_basics",
//       target: "end2",
//     },
//     {
//       id: "e5-8",
//       source: "no_basics",
//       target: "end3",
//     },
//   ],
// };

interface FlowDiagramProps {
  renderJson: any; // Replace 'any' with the appropriate type if known
}

const FlowDiagram = ({ renderJson }: FlowDiagramProps) => {
  const { nodes, edges } = renderJson;
  const [nodesState, setNodesState] = useNodesState(nodes);
  const [edgesState, setEdgesState] = useEdgesState(edges);
  return (
    <div style={{ height: 500, width: "100%" }}>
      <ReactFlow
        nodes={nodesState}
        edges={edgesState.map((edge) => ({
          ...edge,
          type: "straight", // Ensures all edges are straight
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
            type: "straight", // Ensures new connections are straight
            label: prompt("Enter label for the new connection:", "") || "",
            labelBgStyle: {
              fill: "#fff",
              color: "#222",
              strokeWidth: 1,
              stroke: "#222",
            },
            labelStyle: { fontWeight: 700 },
          };
          setEdgesState((eds) => addEdge(newEdge, eds));
        }}
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default FlowDiagram;
