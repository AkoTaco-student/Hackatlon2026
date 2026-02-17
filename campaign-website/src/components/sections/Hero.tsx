import { Link } from "react-router-dom";
import { site } from "@/data/site";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 grid-lines opacity-40" />
      <div className="absolute inset-0 hero-sheen" />
      <div className="container relative z-10 grid gap-8 py-16 md:grid-cols-[1.2fr_0.8fr] md:py-24">
        <div className="space-y-6">
          <Badge variant="accent">Virtuelt kampanjeparti</Badge>
          <h1 className="text-4xl font-semibold leading-tight md:text-5xl">
            {site.tagline}
          </h1>
          <p className="text-base text-muted-foreground md:text-lg">
            {site.description}
          </p>
          <p className="text-sm text-foreground/80">{site.pitch}</p>
          <div className="flex flex-wrap gap-3">
            <Button asChild size="lg">
              <a href={site.primaryCta.href}>{site.primaryCta.label}</a>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link to={site.secondaryCta.href}>{site.secondaryCta.label}</Link>
            </Button>
          </div>
          <div className="flex flex-wrap gap-4 text-xs text-muted-foreground">
            <span>Utdanning + AI</span>
            <span>Første jobb</span>
            <span>Digitalt demokrati</span>
          </div>
        </div>
        <div className="surface flex flex-col gap-4 p-6 shadow-glow">
          <p className="section-kicker">Neste steg</p>
          <p className="text-lg font-semibold">
            Gi unge en tryggere vei inn i fremtidens arbeidsliv.
          </p>
          <ul className="space-y-3 text-sm text-muted-foreground">
            <li>• Kortere vei til første jobb</li>
            <li>• Ansvarlig AI i offentlig sektor</li>
            <li>• Grønn omstilling som funker i hverdagen</li>
          </ul>
          <Button asChild variant="secondary">
            <Link to="/saker">Se sakene våre</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
