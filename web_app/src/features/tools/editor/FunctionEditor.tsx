import React from "react";
import Editor from "@monaco-editor/react";

function FunctionEditor({
  newCode,
  setCode,
}: {
  newCode: string;
  setCode: (newCode: string) => void;
}) {
  return (
    <Editor
      defaultLanguage="python"
      theme="vs-dark"
      defaultValue={newCode}
      onChange={(code: string | undefined) => {
        setCode(code ?? "");
      }}
      options={{
        minimap: {
          enabled: false,
        },
      }}
      className="h-full flex-1"
    />
  );
}

export default FunctionEditor;
