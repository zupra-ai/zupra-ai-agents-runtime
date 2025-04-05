import MainLayout from "@/components/layout/MainLayout";
import ApplicationsFeature from "@/features/apps/ApplicationsFeature";
import TanstackProvider from "@/providers/TanstackProvider";

export default function Page() {
  return (
    <MainLayout>
      <TanstackProvider>
        <ApplicationsFeature />
      </TanstackProvider>
    </MainLayout>
  );
}
