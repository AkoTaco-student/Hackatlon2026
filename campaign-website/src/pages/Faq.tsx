import SectionHeading from "@/components/content/SectionHeading";
import { faq } from "@/data/faq";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

export default function Faq() {
  return (
    <div className="container space-y-12 py-16">
      <SectionHeading
        kicker="FAQ"
        title="Svar på det viktigste"
        description="Fortsatt nysgjerrig? Send oss en melding i kanalene våre."
      />
      <Accordion type="single" collapsible className="surface p-6">
        {faq.map((item) => (
          <AccordionItem key={item.question} value={item.question}>
            <AccordionTrigger>{item.question}</AccordionTrigger>
            <AccordionContent>{item.answer}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
}
