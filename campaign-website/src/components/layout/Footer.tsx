import { Link } from "react-router-dom";
import { site } from "@/data/site";

export default function Footer() {
  return (
    <footer className="border-t border-border/60 bg-background">
      <div className="container grid gap-6 py-10 md:grid-cols-[2fr_1fr_1fr]">
        <div className="space-y-2">
          <p className="font-display text-lg font-semibold">{site.name}</p>
          <p className="text-sm text-muted-foreground">{site.description}</p>
        </div>
        <div className="space-y-2 text-sm">
          <p className="font-semibold">Sider</p>
          <div className="flex flex-col gap-2 text-muted-foreground">
            {site.navigation.map((item) => (
              <Link key={item.href} to={item.href}>
                {item.label}
              </Link>
            ))}
          </div>
        </div>
        <div className="space-y-2 text-sm">
          <p className="font-semibold">Sosialt</p>
          <div className="flex flex-col gap-2 text-muted-foreground">
            {site.socials.map((item) => (
              <a key={item.label} href={item.href}>
                {item.label}
              </a>
            ))}
          </div>
        </div>
      </div>
      <div className="border-t border-border/60 py-4 text-center text-xs text-muted-foreground">
        © 2026 {site.name}. Virtuelt kampanjekonsept.
      </div>
    </footer>
  );
}
