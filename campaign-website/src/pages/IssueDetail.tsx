import { Link, useParams } from "react-router-dom";
import { issues } from "@/data/issues";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function IssueDetail() {
  const { id } = useParams();
  const issue = issues.find((item) => item.id === id);

  if (!issue) {
    return (
      <div className="container py-16">
        <p className="text-lg font-semibold">Fant ikke saken.</p>
        <Button asChild className="mt-4">
          <Link to="/saker">Tilbake til saker</Link>
        </Button>
      </div>
    );
  }

  const Icon = issue.icon;

  return (
    <div className="container space-y-10 py-16">
      <div className="space-y-4">
        <div className="flex items-center gap-3 text-sm text-muted-foreground">
          <Link to="/saker" className="hover:text-foreground">
            Saker
          </Link>
          <span>/</span>
          <span>{issue.title}</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-accent text-primary">
            <Icon className="h-6 w-6" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">{issue.category}</p>
            <h1 className="text-3xl font-semibold">{issue.title}</h1>
          </div>
        </div>
        <p className="max-w-2xl text-muted-foreground">{issue.summary}</p>
        <div className="flex flex-wrap gap-2">
          {issue.tags.map((tag) => (
            <Badge key={tag} variant="accent">
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-[1.3fr_0.7fr]">
        <div className="surface p-6">
          <h2 className="text-lg font-semibold">Hva vi vil oppnå</h2>
          <p className="mt-2 text-sm text-muted-foreground">{issue.impact}</p>
          <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
            {issue.measures.map((measure) => (
              <li key={measure}>• {measure}</li>
            ))}
          </ul>
        </div>
        <div className="surface p-6">
          <h3 className="text-lg font-semibold">Neste steg</h3>
          <p className="mt-2 text-sm text-muted-foreground">
            Del saken og støtt arbeidet vårt digitalt.
          </p>
          <Button className="mt-4 w-full">Støtt saken</Button>
        </div>
      </div>
    </div>
  );
}
