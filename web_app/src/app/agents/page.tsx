import MainLayout from "@/components/layout/MainLayout";
import AgentsFeature from "@/features/agents/AgentsFeature";
import TanstackProvider from "@/providers/TanstackProvider";

export default function Page() {
  return (
    <MainLayout>
      <TanstackProvider>
        <AgentsFeature />
      </TanstackProvider>
    </MainLayout>
  );
}
