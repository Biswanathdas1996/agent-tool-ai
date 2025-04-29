// FlowDiagram.jsx
import React, { useState } from "react";
import ReactFlow from "reactflow";
import "reactflow/dist/style.css";

const flowData = {
  nodes: [
    {
      id: "start",
      type: "input",
      data: {
        label: "Do you understand flowcharts?",
      },
      position: {
        x: 0,
        y: 0,
      },
    },
    {
      id: "yes_understand",
      data: {
        label: "Great! Visit the Diagram Community for examples and templates.",
      },
      position: {
        x: 300,
        y: 0,
      },
    },
    {
      id: "no_understand",
      data: {
        label: "Would you like to start with the basics?",
      },
      position: {
        x: 0,
        y: 200,
      },
    },
    {
      id: "yes_basics",
      data: {
        label: "Read a complete flowchart guide with examples.",
      },
      position: {
        x: 300,
        y: 200,
      },
    },
    {
      id: "no_basics",
      data: {
        label: "Read more about flowcharts.",
      },
      position: {
        x: 300,
        y: 400,
      },
    },
    {
      id: "end1",
      type: "output",
      data: {
        label: "End",
      },
      position: {
        x: 600,
        y: 0,
      },
    },
    {
      id: "end2",
      type: "output",
      data: {
        label: "End",
      },
      position: {
        x: 600,
        y: 200,
      },
    },
    {
      id: "end3",
      type: "output",
      data: {
        label: "End",
      },
      position: {
        x: 600,
        y: 400,
      },
    },
  ],
  edges: [
    {
      id: "e1-2",
      source: "start",
      target: "yes_understand",
      label: "Yes",
      labelBgStyle: {
        fill: "#fff",
        color: "#222",
        strokeWidth: 1,
        stroke: "#222",
      },
      labelStyle: { fontWeight: 700 },
    },
    {
      id: "e1-3",
      source: "start",
      target: "no_understand",
      label: "No",
      labelBgStyle: {
        fill: "#fff",
        color: "#222",
        strokeWidth: 1,
        stroke: "#222",
      },
      labelStyle: { fontWeight: 700 },
    },
    {
      id: "e3-4",
      source: "no_understand",
      target: "yes_basics",
      label: "Yes",
      labelBgStyle: {
        fill: "#fff",
        color: "#222",
        strokeWidth: 1,
        stroke: "#222",
      },
      labelStyle: { fontWeight: 700 },
    },
    {
      id: "e3-5",
      source: "no_understand",
      target: "no_basics",
      label: "No",
      labelBgStyle: {
        fill: "#fff",
        color: "#222",
        strokeWidth: 1,
        stroke: "#222",
      },
      labelStyle: { fontWeight: 700 },
    },
    {
      id: "e2-6",
      source: "yes_understand",
      target: "end1",
    },
    {
      id: "e4-7",
      source: "yes_basics",
      target: "end2",
    },
    {
      id: "e5-8",
      source: "no_basics",
      target: "end3",
    },
  ],
};

const FlowDiagram = () => {
  const { nodes, edges } = flowData;

  return (
    <div style={{ height: 500, width: "100%" }}>
      <ReactFlow nodes={nodes} edges={edges} fitView />
    </div>
  );
};

export default FlowDiagram;
