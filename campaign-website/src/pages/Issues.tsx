import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { issueCategories, issues } from "@/data/issues";
import IssueCard from "@/components/content/IssueCard";
import SectionHeading from "@/components/content/SectionHeading";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function Issues() {
  const [active, setActive] = useState<(typeof issueCategories)[number]>(
    "Alle"
  );

  const filtered = useMemo(() => {
    if (active === "Alle") return issues;
    return issues.filter((issue) => issue.category === active);
  }, [active]);

  return (
    <div className="container space-y-10 py-16">
      <SectionHeading
        kicker="Saker"
        title="Kort vei til forståelige prioriteringer"
        description="Velg tema og få en rask oversikt over konkrete tiltak."
      />
      <div className="flex flex-wrap gap-3">
        {issueCategories.map((category) => (
          <Button
            key={category}
            variant={category === active ? "default" : "outline"}
            size="sm"
            onClick={() => setActive(category)}
          >
            {category}
          </Button>
        ))}
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        {filtered.map((issue) => (
          <IssueCard key={issue.id} issue={issue} />
        ))}
      </div>
      <div className="surface flex flex-col gap-4 p-6 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Oppsummert program</p>
          <p className="text-lg font-semibold">
            Se helheten bak sakene våre.
          </p>
        </div>
        <Button asChild>
          <Link to="/program">Gå til program</Link>
        </Button>
      </div>
      <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
        <Badge variant="outline">Oppdatert for 2026</Badge>
        <Badge variant="outline">Kortformat</Badge>
      </div>
    </div>
  );
}
