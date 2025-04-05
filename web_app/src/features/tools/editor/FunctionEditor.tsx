import React from "react";
import Editor from "@monaco-editor/react";

function FunctionEditor({
  newCode,
  setCode,
  language = "python",
  readOnly = false,
}: {
  newCode: string;
  language?: string;
  readOnly?: boolean;
  setCode: (newCode: string) => void;
}) {
  return (
    <Editor
      
      defaultLanguage={language}
      theme="vs-dark"
      defaultValue={newCode}
      onChange={(code: string | undefined) => {
        setCode(code ?? "");
      }}
      options={{
        readOnly: readOnly,
        minimap: {
          enabled: false,
        },
      }}
      className="h-full flex-1"
    />
  );
}

export default FunctionEditor;
