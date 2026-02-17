import Hero from "@/components/sections/Hero";
import IssuesPreview from "@/components/sections/IssuesPreview";
import Values from "@/components/sections/Values";
import ProgramCTA from "@/components/sections/ProgramCTA";
import TeamPreview from "@/components/sections/TeamPreview";
import FaqPreview from "@/components/sections/FaqPreview";
import JoinBanner from "@/components/sections/JoinBanner";

export default function Home() {
  return (
    <div>
      <Hero />
      <IssuesPreview />
      <Values />
      <ProgramCTA />
      <TeamPreview />
      <FaqPreview />
      <JoinBanner />
    </div>
  );
}
