import SectionHeading from "@/components/content/SectionHeading";

const values = [
  {
    title: "Fremtidsrettet",
    description: "Politikk som tar høyde for AI, cybersikkerhet og raske skifter.",
  },
  {
    title: "Rettferdig",
    description: "Teknologi skal redusere ulikhet og styrke fellesskapet.",
  },
  {
    title: "Praktisk",
    description: "Tiltak som faktisk fungerer i student- og arbeidshverdagen.",
  },
];

export default function Values() {
  return (
    <section className="container space-y-8 py-16">
      <SectionHeading
        kicker="Hvorfor oss"
        title="Vi er partiet for overgangsfasen"
        description="Når du går fra studie til jobb, skal samfunnet heie på deg."
      />
      <div className="grid gap-6 md:grid-cols-3">
        {values.map((value) => (
          <div key={value.title} className="surface p-6">
            <h3 className="text-lg font-semibold">{value.title}</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              {value.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
