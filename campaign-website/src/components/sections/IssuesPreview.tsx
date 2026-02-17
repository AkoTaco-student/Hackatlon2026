import { Link } from "react-router-dom";
import { issues } from "@/data/issues";
import SectionHeading from "@/components/content/SectionHeading";
import IssueCard from "@/components/content/IssueCard";
import { Button } from "@/components/ui/button";

export default function IssuesPreview() {
  return (
    <section className="container space-y-8 py-16">
      <SectionHeading
        kicker="Våre hovedsaker"
        title="Det vi kjemper for nå"
        description="Kort, konkret og gjennomførbart."
      />
      <div className="grid gap-6 md:grid-cols-3">
        {issues.slice(0, 3).map((issue) => (
          <IssueCard key={issue.id} issue={issue} />
        ))}
      </div>
      <Button asChild variant="outline">
        <Link to="/saker">Se alle saker</Link>
      </Button>
    </section>
  );
}
