import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

import React, { useEffect } from "react";
import ToolModel from "@/models/ToolModel";
import { useOneTools } from "@/api_hooks/useOneTools";
import EditorLayout from "../editor/EditorLayout";
import { FunctionSquare } from "lucide-react";

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
            <SheetTitle className="flex items-center gap-2">
              {" "}
              <FunctionSquare /> {data?.name}
            </SheetTitle>
          </SheetHeader>

          {data && <EditorLayout tool={data} />}
        </SheetContent>
      )}
    </Sheet>
  );
}

export default ToolForm;
