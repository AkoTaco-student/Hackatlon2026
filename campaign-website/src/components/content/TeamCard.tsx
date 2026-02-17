import { Card, CardContent } from "@/components/ui/card";

type Props = {
  name: string;
  role: string;
  bio: string;
};

export default function TeamCard({ name, role, bio }: Props) {
  return (
    <Card>
      <CardContent className="space-y-3">
        <div>
          <p className="text-base font-semibold">{name}</p>
          <p className="text-sm text-muted-foreground">{role}</p>
        </div>
        <p className="text-sm text-muted-foreground">{bio}</p>
      </CardContent>
    </Card>
  );
}
