import MainLayout from "@/components/layout/MainLayout";
import ToolsFeature from "@/features/tools/ToolsFeature";
import TanstackProvider from "@/providers/TanstackProvider";

export default function Page() {
  return (
    <MainLayout>
      <TanstackProvider>
        <ToolsFeature />
      </TanstackProvider>
    </MainLayout>
  );
}
