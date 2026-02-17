import { Button } from "@/components/ui/button";

export default function JoinBanner() {
  return (
    <section id="bli-med" className="container py-16">
      <div className="surface grid gap-6 p-8 md:grid-cols-[1.3fr_0.7fr]">
        <div className="space-y-2">
          <p className="section-kicker">Bli med</p>
          <h2 className="text-2xl font-semibold">
            Del idéer, test politikk og bygg fremtidens Norge.
          </h2>
          <p className="text-sm text-muted-foreground">
            Vi bygger arenaer der studenter jobber med reelle digitaliseringsoppdrag
            sammen med akademia, offentlig sektor og teknologimiljøer.
          </p>
        </div>
        <div className="flex items-center md:justify-end">
          <Button size="lg">Registrer interesse</Button>
        </div>
      </div>
    </section>
  );
}
