import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

import React, { useEffect } from "react";
import FunctionEditor from "../editor/FunctionEditor";
import ToolModel from "@/models/ToolModel";
import { useOneTools } from "@/api_hooks/useOneTools";

function ToolForm({
  tool,
  onOpenChange,
}: {
  tool: ToolModel | null;
  onOpenChange: (open: boolean) => void;
}) {
  const { data, isLoading } = useOneTools(tool?.id ?? "");

  useEffect(() => {
    if (tool) {
      console.log("ToolForm", tool);
    }
  }, [tool]);

  if (isLoading) return <div>Loading...</div>;

  return (
    <Sheet open={!!tool} onOpenChange={onOpenChange}>
      {isLoading ? (
        <SheetContent className="w-full lg:min-w-[calc(100vw-80px)]">
        <div>Loading...</div>
        </SheetContent>
      ) : (
        <SheetContent className="w-full lg:min-w-[calc(100vw-80px)]">
          <SheetHeader>
            <SheetTitle>Are you absolutely sure?</SheetTitle>
            <SheetDescription>
              This action cannot be undone. This will permanently delete your
              account and remove your data from our servers.
            </SheetDescription>
          </SheetHeader>

          <FunctionEditor newCode={data?.body ?? ""} setCode={() => {}} />
        </SheetContent>
      )}
    </Sheet>
  );
}

export default ToolForm;
