import SectionHeading from "@/components/content/SectionHeading";
import TeamCard from "@/components/content/TeamCard";
import { team } from "@/data/team";
import { Button } from "@/components/ui/button";

export default function Team() {
  return (
    <div className="container space-y-12 py-16">
      <SectionHeading
        kicker="Team"
        title="Kort vei til beslutninger"
        description="Vi jobber digitalt og åpent for å nå unge over hele landet, og samarbeider tett med kompetansemiljøer."
      />
      <div className="grid gap-6 md:grid-cols-2">
        {team.map((member) => (
          <TeamCard key={member.name} {...member} />
        ))}
      </div>
      <div className="surface flex flex-col gap-4 p-6 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Vil du bidra?</p>
          <p className="text-lg font-semibold">Bli med i arbeidsgruppene våre.</p>
        </div>
        <Button>Registrer interesse</Button>
      </div>
    </div>
  );
}
