import React from "react";
import { ParentSize } from "@visx/responsive";
import Example from "../../components/timeline";

const Timeline = () => {
  return (
    <ParentSize>
      {({ width, height }) => <Example width={width} height={height} />}
    </ParentSize>
  );
};

export default Timeline;
