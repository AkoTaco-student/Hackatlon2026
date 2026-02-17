import SectionHeading from "@/components/content/SectionHeading";
import { principles, programThemes } from "@/data/program";
import { Card, CardContent } from "@/components/ui/card";

export default function Program() {
  return (
    <div className="container space-y-12 py-16">
      <SectionHeading
        kicker="Program"
        title="Kortversjonen av vår politikk"
        description="Vi prioriterer tiltak som gir rask effekt for studenter og unge arbeidstakere, i tett samarbeid med teknologi- og kunnskapsmiljøer."
      />
      <div className="grid gap-6 md:grid-cols-2">
        {principles.map((principle) => (
          <Card key={principle.title}>
            <CardContent className="space-y-2">
              <h3 className="text-lg font-semibold">{principle.title}</h3>
              <p className="text-sm text-muted-foreground">
                {principle.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="space-y-6">
        <SectionHeading
          kicker="Tema"
          title="Prioriterte områder"
          description="Hvert punkt er valgt for å gi raske og målbare resultater."
        />
        <div className="grid gap-6 md:grid-cols-2">
          {programThemes.map((theme) => (
            <Card key={theme.title}>
              <CardContent className="space-y-3">
                <h3 className="text-lg font-semibold">{theme.title}</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  {theme.points.map((point) => (
                    <li key={point}>• {point}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
