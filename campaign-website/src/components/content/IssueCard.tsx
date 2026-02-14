import { Link } from "react-router-dom";
import { Issue } from "@/data/issues";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function IssueCard({ issue }: { issue: Issue }) {
  const Icon = issue.icon;

  return (
    <Card className="h-full transition hover:-translate-y-1 hover:shadow-lg">
      <CardHeader className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-accent text-primary">
            <Icon className="h-5 w-5" />
          </div>
          <Badge variant="outline">{issue.category}</Badge>
        </div>
        <CardTitle>{issue.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground">{issue.summary}</p>
        <div className="flex flex-wrap gap-2">
          {issue.tags.map((tag) => (
            <Badge key={tag} variant="accent">
              {tag}
            </Badge>
          ))}
        </div>
        <Link
          to={`/saker/${issue.id}`}
          className="text-sm font-semibold text-primary"
        >
          Les mer
        </Link>
      </CardContent>
    </Card>
  );
}
