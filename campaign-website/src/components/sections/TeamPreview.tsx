import SectionHeading from "@/components/content/SectionHeading";
import TeamCard from "@/components/content/TeamCard";
import { team } from "@/data/team";

export default function TeamPreview() {
  return (
    <section className="container space-y-8 py-16">
      <SectionHeading
        kicker="Team"
        title="Mennesker som gjør jobben"
        description="Et lite team med stort ansvar og tette bånd til teknologi- og rådgivningsmiljøer."
      />
      <div className="grid gap-6 md:grid-cols-2">
        {team.slice(0, 2).map((member) => (
          <TeamCard key={member.name} {...member} />
        ))}
      </div>
    </section>
  );
}
