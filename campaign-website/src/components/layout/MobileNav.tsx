import { Link } from "react-router-dom";
import { Menu } from "lucide-react";
import { site } from "@/data/site";
import { Button } from "@/components/ui/button";
import { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";

export default function MobileNav() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline" size="sm" aria-label="Åpne meny">
          <Menu className="h-4 w-4" />
        </Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>{site.name}</SheetTitle>
        </SheetHeader>
        <div className="flex flex-col gap-4 text-sm">
          {site.navigation.map((item) => (
            <Link key={item.href} to={item.href} className="font-medium">
              {item.label}
            </Link>
          ))}
          <div className="mt-4 flex flex-col gap-3">
            <Button asChild variant="outline">
              <Link to="/program">Les programmet</Link>
            </Button>
            <Button asChild>
              <a href={site.primaryCta.href}>{site.primaryCta.label}</a>
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
