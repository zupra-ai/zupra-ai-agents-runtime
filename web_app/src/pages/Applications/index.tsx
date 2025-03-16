import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppWindow } from "lucide-react";
import ApplicationsTable from "./partial/table";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const queryClient = new QueryClient();

function ApplicationsPage() {
  const [open, setOpen] = useState(false);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex-1 flex flex-col">
        <div className="flex gap-x-2 sticky">
          <div className="w-16 h-16 bg-slate-100 flex items-center justify-center">
            <AppWindow size="38" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-semibold uppercase">
              Applications List
            </h2>
            <p className="text-sm text-slate-800">Applications List</p>
          </div>
          <div className="flex gap-2">
            <Button onClick={() => setOpen(true)}>Add New</Button>
            <Button variant="outline">Edit</Button>
          </div>
        </div>
        <div className="h-6" />

        <Sheet open={open} onOpenChange={(open) => setOpen(open)}>
          <SheetContent>
            <SheetHeader>
              <SheetTitle>New Application</SheetTitle>
              <SheetDescription>
                <Label>Name</Label>
                <Input />
              </SheetDescription>
            </SheetHeader>
          </SheetContent>
        </Sheet>

        <div className="flex-1 flex flex-col ">
          <ApplicationsTable />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default ApplicationsPage;
