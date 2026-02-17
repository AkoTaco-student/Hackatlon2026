import { Link } from "react-router-dom";
import SectionHeading from "@/components/content/SectionHeading";
import { Button } from "@/components/ui/button";

export default function ProgramCTA() {
  return (
    <section className="container py-16">
      <div className="surface grid gap-6 p-8 md:grid-cols-[1.2fr_0.8fr]">
        <SectionHeading
          kicker="Program"
          title="Kort, tydelig og gjennomførbart"
          description="Se hvordan vi prioriterer utdanning, jobb og grønn omstilling."
        />
        <div className="flex items-center md:justify-end">
          <Button asChild size="lg">
            <Link to="/program">Les hele programmet</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
