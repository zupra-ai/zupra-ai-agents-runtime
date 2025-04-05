import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";

import React, { useEffect } from "react";
import ToolModel from "@/models/ToolModel";
import FunctionEditor from "./FunctionEditor";
import { useOneTools } from "@/api_hooks/useOneTools";

function EditorLayout({ tool }: { tool: ToolModel | null }) {
  const { data, isLoading } = useOneTools(tool?.id ?? "");

  useEffect(() => {
    if (tool) {
      console.log("ToolForm", tool);
    }
  }, [tool]);

  if (isLoading) return <div>Loading...</div>;

  return (
    <PanelGroup direction="horizontal">
      <Panel defaultSize={80}>
        <PanelGroup direction="vertical">
          <Panel defaultSize={80}>
            <FunctionEditor newCode={data?.body ?? ""} setCode={() => {}} />
          </Panel>
          <PanelResizeHandle className="h-1 bg-amber-600" />
          <Panel defaultSize={20}>
            <FunctionEditor readOnly newCode={""} setCode={() => {}} />
          </Panel>
        </PanelGroup>
      </Panel>
      <PanelResizeHandle className="w-1 bg-amber-600" />
      <Panel defaultSize={20}>
        <FunctionEditor language="markdown" newCode={data?.requirements ?? ""} setCode={() => {}} />
      </Panel>
    </PanelGroup>
  );
}

export default EditorLayout;
