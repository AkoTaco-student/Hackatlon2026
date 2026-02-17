import { Link } from "react-router-dom";
import SectionHeading from "@/components/content/SectionHeading";
import { faq } from "@/data/faq";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";

export default function FaqPreview() {
  return (
    <section className="container space-y-8 py-16">
      <SectionHeading
        kicker="FAQ"
        title="Spørsmål vi ofte får"
        description="Kort svar nå, full oversikt på egen side."
      />
      <Accordion type="single" collapsible className="surface p-6">
        {faq.slice(0, 3).map((item) => (
          <AccordionItem key={item.question} value={item.question}>
            <AccordionTrigger>{item.question}</AccordionTrigger>
            <AccordionContent>{item.answer}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
      <Button asChild variant="outline">
        <Link to="/faq">Se alle spørsmål</Link>
      </Button>
    </section>
  );
}
