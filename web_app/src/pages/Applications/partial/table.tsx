import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Application } from "../types";
import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";
  
  
  
  
  const ApplicationsTable = () => {
  const [page] = useState(0);

  const { isPending, error, data } = useQuery({
    queryKey: ["data", { page }],
    queryFn: () =>
      fetch(`${import.meta.env.VITE_API_HOST}/applications?page=${page}`).then(
        (res) => res.json()
      ),
  });

  if (isPending) return "loading...";

  if (error) return "An error has occurred: " + error.message;

  const _list = data.data as Application[];

  return (
    <div className="flex-1">
      <Table>
        <TableCaption>App List</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Trait App</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {_list.map((i, index) => (
            <TableRow key={index}>
              <TableCell className="font-medium">{i.id}</TableCell>
              <TableCell>{i.name}</TableCell>
              <TableCell>{i.description}</TableCell>
              <TableCell className="text-right">
                <Button size="icon" variant="ghost" onClick={() => {}}>
                  <Menu />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};


export default ApplicationsTable